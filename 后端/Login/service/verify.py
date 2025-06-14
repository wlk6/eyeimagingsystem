from Login import models


class DoctorData:
    def __init__(self, doctor: dict):
        self.doctor = doctor

    def returnData(self):
        self.doctor.pop("password")
        return self.doctor


class AdminData:
    def __init__(self, admin: dict):
        self.admin = admin

    def returnData(self):
        self.admin.pop("password")
        return self.admin


def DoctorLoginVerify(doctor_id,password):
    if doctor_id is None:
        return {"msg": "请输入医生工作编号"}
    if password is None:
        return {"msg": "请输入密码"}
    doctor = models.doctor.objects.filter(doctor_id=doctor_id, password=password).values().first()
    if doctor:
        # 隐藏用户的一些信息
        doctorData = DoctorData(doctor=doctor).returnData()
        return {"msg": "登录成功", "data": doctorData}
    else:
        return {"msg": "工作编号或者密码错误,请联系管理员确定账号信息"}


def AdminLoginVerify(admin_id,password):
    if admin_id is None:
        return {"msg": "请输入管理员工作编号"}
    if password is None:
        return {"msg": "请输入密码"}
    admin = models.admin.objects.filter(admin_id=admin_id, password=password).values().first()
    if admin:
        # 隐藏用户的一些信息
        adminData = AdminData(admin=admin).returnData()
        return {"msg": "登录成功", "data": adminData}
    else:
        return {"msg": "工作编号或者密码错误,请确定账号信息是否正确"}
