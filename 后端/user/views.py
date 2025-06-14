import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from Login.models import doctor, checkInfo
from Login.service.jwt import IsDoctor, IsAdmin, IsDoctorOrAdmin
from Login.service.serializers import addDoctorSerializer, doctorAlterInfoSerializer, checkInfoSerializer, \
    afterCheckSerializer, getDoctorListSerializer, getDorctorInfoSerializer
from user.models import patient, DoctorPatientRelation
from user.serializers import PatientSerializer


# Create your views here.
class PatientView(APIView):
    permission_classes = [IsDoctor]

    def get(self, request, *args, **kwargs):
        """
        获取所有患者信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        patients = patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        添加患者信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # doctor_id = getattr(request.user, 'doctor_id', None)
        # patient_id = request.data.get('patient_id')
        # if not doctor_id:
        #     return Response({'error': '医生 ID 不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        # if not patient_id:
        #     return Response({'error': '患者 ID 不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        #
        # print(f"request.user: {request.user}")
        # print(f"request.user.id: {getattr(request.user, 'id', None)}")  # 打印用户 ID

        doctor_id = request.data.get('doctor_id')

        patient_id = request.data.get('patient_id')
        patients = request.data
        if patient.objects.filter(patient_id=patient_id).exists():
            return Response({"error": "患者已存在"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PatientSerializer(data=patients)
        if serializer.is_valid():
            data = serializer.save()
            patient_id = data.patient_id

            relation = DoctorPatientRelation.objects.create(doctor_id=doctor_id, patient_id=patient_id)

            # 返回成功响应
            return Response(
                {
                    'msg': '成功添加患者信息并建立医患关系',
                    'data': serializer.data,
                    'relation': {

                        "doctor_id": doctor_id,
                        "patient_id": patient_id
                    }
                },
                status=status.HTTP_201_CREATED
            )
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailView(APIView):
    permission_classes = [IsDoctor]

    def post(self, request, *args, **kwargs):
        """
        查找患者信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        patient_id = request.data.get('patient_id')
        try:
            patients = patient.objects.get(patient_id=patient_id)
            serializer = PatientSerializer(patients)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except patient.DoesNotExist:
            return Response({'error': '未找到该患者'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        """
        更新患者信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        patient_id = request.data.get('patient_id')

        if not patient_id:
            return Response(
                {'error': 'ID不在请求参数中'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            patients = patient.objects.get(patient_id=patient_id)
        except patient.DoesNotExist:
            return Response(
                {'error': '未找到该患者'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PatientSerializer(patients, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'msg': '更新成功',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

    def delete(self, request, *args, **kwargs):
        patient_id = request.data.get('patient_id')

        patient.objects.get(pk=patient_id).delete()
        return Response({'msg': '删除成功'}, status=status.HTTP_200_OK)


# 管理员添加医生账号
class adminAddDoctorAccount(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            serializer = addDoctorSerializer(data=request.data)
            if serializer.is_valid():
                # print(serializer)
                serializer.save()
                serializer_data = dict(serializer.data)
                serializer_data.pop('password', None)
                return Response({'code': 200, 'msg': '添加医生账号成功', 'data': serializer_data})
            return Response({'code': 404, 'msg': serializer.errors})
        except Exception as e:  # 捕获与处理异常
            return Response({'code': 404, 'msg': f"系统错误{e}"})


class getDoctorListView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            doctorList = doctor.objects.filter()
            serializer = getDoctorListSerializer(instance=doctorList, many=True)
            return Response({'code': 200, 'msg': "获取医生列表成功", 'data': serializer.data})
        except Exception as e:  # 捕获与处理异常
            return Response({'code': 404, 'msg': f"系统错误{e}"})


# 管理员获取待审核医生信息列表
class adminGetCheckList(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            checkList = checkInfo.objects.filter(result=0, is_password=0).order_by('alter_time')
            serializer = checkInfoSerializer(instance=checkList, many=True)
            return Response({'code': 200, 'msg': "获取待审核医生信息列表成功", 'data': serializer.data})
        except Exception as e:  # 捕获与处理异常
            return Response({'code': 404, 'msg': f"系统错误{e}"})


# 管理员获取医生信息详情
class adminCheckDoctorInfo(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            doctor_id = request.data.get('doctor_id')
            checkDetail = checkInfo.objects.filter(doctor_id=doctor_id).first()
            if checkDetail is None:
                return Response({'code': 404, 'msg': "该审核信息不存在"})
            serializer = checkInfoSerializer(instance=checkDetail)
            return Response({'code': 200, 'msg': "获取待审核医生信息详情成功", 'data': serializer.data})
        except Exception as e:  # 捕获与处理异常
            return Response({'code': 404, 'msg': f"系统错误{e}"})


# 管理员给出审核结果
class adminGiveCheckAdvice(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            doctor_id = request.data.get('doctor_id')
            result = request.data.get('result')
            advice = request.data.get('advice')
            checkDetail = checkInfo.objects.filter(result=0, is_password=0, doctor_id=doctor_id).first()
            if result is None:
                return Response({'code': 404, 'msg': "未输入审核结果"})
            if result == 0:
                # checkDetail.advice = advice
                # instance参数标识要操作的现有模型实例，例如从数据库中查询出来的对象，用于更新操作
                # data表示原始数据，用于创建新对象活验证数据，当需要验证数据但是不保存是也可以单独使用data
                print(checkDetail)
                serializer = afterCheckSerializer(instance=checkDetail, data={'advice': advice,'result':-1}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'code': 200, 'msg': "审核医生信息成功", 'data': serializer.data})
                else:
                    return Response({'code': 400, 'msg': "审核医生信息失败", 'data': serializer.errors})
            if result == 1:
                serializer = afterCheckSerializer(instance=checkDetail,
                                                  data={'result': 1, 'check_time': datetime.datetime.now()},
                                                  partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response({'code': 400, 'msg': "审核医生信息失败", 'data': serializer.errors})
                # 创建了新实例而不是获取已有医生
                # Doctor = doctor()
                Doctor = doctor.objects.filter(doctor_id=doctor_id).first()
                Doctor.doctor_id = checkDetail.doctor_id
                if checkDetail.doctor_name:
                    Doctor.doctor_name = checkDetail.doctor_name
                if checkDetail.phone:
                    Doctor.phone = checkDetail.phone
                if checkDetail.email:
                    Doctor.email = checkDetail.email
                if checkDetail.gender:
                    Doctor.gender = checkDetail.gender
                if checkDetail.position:
                    Doctor.position = checkDetail.position
                if checkDetail.avatar:
                    Doctor.avatar = checkDetail.avatar
                # serializer = alterDoctorSerializer(instance=Doctor)
                # print(serializer.data)
                # if serializer.is_valid():
                Doctor.save()
                return Response({'code': 200, 'msg': "审核医生信息成功"})
        except Exception as e:  # 捕获与处理异常
            return Response({'code': 404, 'msg': f"系统错误{e}"})


# 管理员删除医生
class adminDelDoctorAccount(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        doctor_id = request.data.get('doctor_id')
        if not doctor_id:
            return Response({'code': 404, 'msg': '医生编号不能为空'})
        try:
            Doctor = doctor.objects.filter(doctor_id=doctor_id).first()
            if Doctor:
                Doctor.delete()
                return Response({'code': 200, 'msg': '医生信息删除成功'})
            else:
                return Response({'code': 404, 'msg': '未找到指定的医生账号'})
        except Exception as e:
            return Response({'code': 404, 'msg': f"系统错误{e}"})


# 医生提交更改信息的申请
class doctorAlterInfo(APIView):
    permission_classes = [IsDoctor]

    def post(self, request):
        # try:
            doctor_id = request.user.doctor_id
            Doctor = doctor.objects.filter(doctor_id=doctor_id).first()
            doctor_info = checkInfo.objects.filter(doctor_id=doctor_id).first()
            if Doctor is None:
                return Response({'code': 404, 'msg': '用户不存在'})
            data = request.data.copy()
            data.update({'doctor_id': doctor_id, 'is_password': 0, 'result': 0, 'alter_time': datetime.datetime.now()})
            if not doctor_info:
                serializer = doctorAlterInfoSerializer(data=data)
            else:
                doctor_info.phone = None
                doctor_info.email = None
                doctor_info.gender = None
                doctor_info.position = None
                doctor_info.avatar = None
                serializer = doctorAlterInfoSerializer(instance=doctor_info, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'code': 200, 'msg': '修改信息提交成功，请等待管理员审核'})
            return Response({'code': 404, 'msg': serializer.errors})
        # except Exception as e:
        #     return Response({'code': 404, 'msg': f"系统错误{e}"})


# 获取医生个人信息
class getDoctorInfo(APIView):
    permission_classes = [IsDoctorOrAdmin]

    def post(self, request):
        try:
            doctor_id = request.data.get('doctor_id')
            Doctor = doctor.objects.filter(doctor_id=doctor_id).first()
            serializer = doctorAlterInfoSerializer(instance=Doctor)
            return Response({'code': 200, 'msg': '获取医生个人信息成功', 'data': serializer.data})
        except Exception as e:
            return Response({'code': 404, 'msg': f"系统错误{e}"})


# 根据工号、姓名、性别、职位查询医生信息
class selectDoctor(APIView):
    permission_classes = [IsDoctorOrAdmin]

    def post(self, request):
        try:
            doctor_id = request.data.get('doctor_id')
            doctor_name = request.data.get('doctor_name')
            gender = request.data.get('gender')
            position = request.data.get('position')
            if not doctor_id and not doctor_name and not gender and not position:
                Doctor = doctor.objects.filter().all()
            else:
                # 构建查询条件字典
                query = {}
                if doctor_id:
                    query['doctor_id'] = doctor_id
                if doctor_name:
                    query['doctor_name'] = doctor_name
                if gender:
                    query['gender'] = gender
                if position:
                    query['position'] = position
                Doctor = doctor.objects.filter(**query).all()
            if Doctor is None:
                return Response({'code': 404, 'msg': "未找到相应信息的医生"})
            print(Doctor)
            serializer = getDorctorInfoSerializer(instance=Doctor, many=True)
            return Response({'code': 200, 'msg': '获取医生个人信息成功', 'data': serializer.data})
        except Exception as e:
            return Response({'code': 404, 'msg': f"系统错误{e}"})
