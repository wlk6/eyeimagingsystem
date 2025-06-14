# 签发token
from datetime import datetime, timedelta
import jwt
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from medical_imaging import settings
from datetime import timedelta, datetime


# 自定义用户模型类
class JWTUser:
    def __init__(self, payload):
        self.admin_id = payload.get('admin_id')
        self.doctor_id = payload.get('doctor_id')
        self.is_authenticated = True  # 关键属性
        self.is_admin = self.admin_id is not None
        self.is_doctor = self.doctor_id is not None


# 局部认证
class JWTQueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):

        # 获取token
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise AuthenticationFailed({"code": 401, "msg": "登录成功后才能访问"})
        # 切割
        # 解密payload，判断是否过期
        # 验证第三段的合法性
        salt = settings.SECRET_KEY
        try:
            payload = jwt.decode(jwt=token, key=salt, algorithms=["HS256"], verify=True)
            user = JWTUser(payload)
            # return payload, token
            return user, token
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({"code": 401, "msg": "token已失效"})
        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed({"code": 401, "msg": "token认证失败"})
        except jwt.exceptions.InvalidTokenError:
            raise AuthenticationFailed({"code": 401, "msg": "非法的token"})
        except Exception as e:
            print(f"Unexpected error: {e}")  # 打印其他异常
            raise AuthenticationFailed({"code": 500, "msg": "服务器内部错误"})


def create_token(payload):
    salt = settings.SECRET_KEY
    # 构造Header，默认如下
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    jwt_token = jwt.encode(headers=headers, payload=payload, key=salt, algorithm='HS256')
    return jwt_token


# 权限控制
class IsAdmin(BasePermission):
    """仅允许管理员访问"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)


class IsDoctor(BasePermission):
    """仅允许医生访问"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_doctor)


class IsDoctorOrAdmin(BasePermission):
    """允许医生或管理员访问"""

    def has_permission(self, request, view):
        return bool(
            (request.user and request.user.is_doctor) or
            (request.user and request.user.is_admin)
        )
