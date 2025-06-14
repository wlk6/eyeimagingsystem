import base64
import datetime
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Login.models import checkInfo, doctor
from Login.service import verify
from Login.service.jwt import IsAdmin
from Login.service.serializers import alterPasswordSerializer, checkPasswordSerializer, afterCheckPasswordSerializer
from Login.utils.captcha import Captcha
from Login.service.jwt import create_token, JWTQueryParamsAuthentication
from Login.utils.encrpty import md5


# 医生登录接口
class doctorLoginView(APIView):
    authentication_classes = []  # 取消全局认证

    def post(self, request):
        try:
            doctor_id = request.data.get('ID')
            password = request.data.get('password')
            user_obj = verify.DoctorLoginVerify(doctor_id=doctor_id, password=md5(password))
            if user_obj.get("msg") == "登录成功":
                payload = {
                    'doctor_id': user_obj["data"].get('doctor_id'),  # 自定义用户ID
                    'doctor_name': user_obj["data"].get('doctor_name'),  # 自定义用户名
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=20),  # 设置超时时间，暂时设置为20天
                }

                jwt_token = create_token(payload=payload)
                msg = user_obj.get("msg")
                return Response({'code': 200, 'msg': msg, 'token': jwt_token})
            else:
                return Response({'code': 404, 'msg': user_obj.get("msg")})
        except Exception as e:
            return Response({'code': 404, 'msg': str(e)})


class GetDoctorIdView(APIView):
    """
    获取医生ID的接口
    """
    authentication_classes = [JWTQueryParamsAuthentication]

    def get(self, request):
        try:
            # 从 request.user 中获取 doctor_id
            doctor_id = request.user.get('doctor_id')
            return Response({'msg': '获取成功', 'doctor_id': doctor_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#  管理员登录接口
class adminLoginView(APIView):
    authentication_classes = []  # 取消全局认证

    def post(self, request):
        try:
            admin_id = request.data.get('ID')
            password = request.data.get('password')
            user_obj = verify.AdminLoginVerify(admin_id=admin_id, password=md5(password))
            if user_obj.get("msg") == "登录成功":
                payload = {
                    'admin_id': user_obj["data"].get('admin_id'),  # 自定义用户ID
                    'admin_name': user_obj["data"].get('admin_name'),  # 自定义用户名
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=20),  # 设置超时时间，暂时设置为20天
                }
                jwt_token = create_token(payload=payload)
                msg = user_obj.get("msg")
                return Response({'code': 200, 'msg': msg, 'token': jwt_token})
            else:
                return Response({'code': 404, 'msg': user_obj.get("msg")})
        except Exception as e:
            return Response({'code': 404, 'msg': str(e)})


# 提交修改密码申请
class alterPasswordView(APIView):
    authentication_classes = []  # 取消全局认证

    def post(self, request):
        try:
            doctor_id = request.data.get('doctor_id')
            check_instance = checkInfo.objects.filter(doctor_id=doctor_id).first()
            data = request.data.copy()
            data.update({'is_password': 1, 'result': 0, 'alter_time': datetime.datetime.now()})
            # 初始化序列化器，区分创建和更新场景
            if check_instance:
                # 已有记录：更新操作
                print(data)
                serializer = alterPasswordSerializer(
                    instance=check_instance,  # 传递实例以触发更新
                    data=data
                )
            else:
                serializer = alterPasswordSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'code': 200, 'msg': '密码修改申请已提交'})
            else:
                return Response({'code': 400, 'msg': serializer.errors}, status=400)
        except Exception as e:
            return Response({'code': 404, 'msg': str(e)})


# 管理员获取待审核的修改密码申请列表
class checkPasswordView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            checkList = checkInfo.objects.filter(result=0, is_password=1).order_by('alter_time')
            serializer = checkPasswordSerializer(instance=checkList, many=True)
            # print(serializer.data)
            return Response({'code': 200, 'msg': "获取待审核医生修改密码列表成功", 'data': serializer.data})
        except Exception as e:  # 捕获与处理异常
            return Response({'code': 404, 'msg': f"系统错误{e}"})


# 管理员给出密码审核结果
class adminGivePasswordCheckAdvice(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            doctor_id = request.data.get('doctor_id')
            result = request.data.get('result')
            advice = request.data.get('advice')
            checkDetail = checkInfo.objects.filter(doctor_id=doctor_id, result=0).first()
            if result is None:
                return Response({'code': 404, 'msg': "未输入审核结果"})
            # 下面的result是管理员给出的审核结果
            if result == 0:
                serializer = afterCheckPasswordSerializer(instance=checkDetail, data={'advice': advice, 'check_time': datetime.datetime.now(), 'result': 1}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'code': 200, 'msg': "审核不通过", 'data': serializer.data})
                else:
                    return Response({'code': 400, 'msg': "审核有误", 'data': serializer.errors})
            if result == 1:
                serializer = afterCheckPasswordSerializer(instance=checkDetail, data={'check_time': datetime.datetime.now(),'result': 1}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response({'code': 400, 'msg': "审核医生信息失败", 'data': serializer.errors})
                Doctor = doctor.objects.filter(doctor_id=doctor_id).first()
                Doctor.password = serializer.data.get('password')
                Doctor.save()
                return Response({'code': 200, 'msg': "医生密码修改成功"})
        except Exception as e:  # 捕获与处理异常
            return Response({'code': 404, 'msg': f"系统错误{e}"})


# 生成图片验证码
class ImageCodeView(APIView):
    authentication_classes = []

    def post(self, request):
        captcha = Captcha()
        key, image_data = captcha.create_captcha()
        code = cache.get(key)
        return Response({
            "code": 200,
            "key": key,
            "image_code": code,
            "image": "data:image/png;base64," + base64.b64encode(image_data).decode('utf-8')
        })
