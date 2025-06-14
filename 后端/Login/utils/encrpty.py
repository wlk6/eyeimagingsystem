import hashlib
from django.conf import settings


def md5(password: str):
    # 使用md5算法创建hash对象
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    # 将密码转换为字节串并更新
    obj.update(password.encode('utf-8'))
    return obj.hexdigest()