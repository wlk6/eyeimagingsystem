from django.db import models

# Create your models here.
positions = [
    ('chief_physician', '主任医师'),
    ('associate_physician', '副主任医师'),
    ('attending_doctor', '主治医师')
]


class doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    doctor_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    gender = models.CharField(max_length=6)
    position = models.CharField(max_length=20, choices=positions, default="attending_doctor")  # 职位
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True, verbose_name='头像')
    introduce = models.TextField(null=True, blank=True)  # 简介

    def __str__(self):
        return self.doctor_name

    class Meta:
        db_table = 'doctor'


class admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.admin_name

    class Meta:
        db_table = 'admin'


class checkInfo(models.Model):
    check_info_id = models.AutoField(primary_key=True)
    doctor_id = models.IntegerField()
    doctor_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    phone = models.CharField(null=True, max_length=15)
    email = models.EmailField(null=True, blank=True)
    gender = models.CharField(null=True, max_length=6)
    position = models.CharField(null=True, max_length=20, choices=positions)  # 职位
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True, verbose_name='头像')
    introduce = models.TextField(null=True, blank=True)
    is_password = models.IntegerField(default=0)  # 是否修改了密码，默认没有
    result = models.IntegerField(default=0)  # 审核结果
    advice = models.CharField(max_length=128, null=True)  # 审核建议
    alter_time = models.DateTimeField(blank=True)  # 提交申请时间
    check_time = models.DateTimeField(blank=True, null=True)  # 审核时间

    def __str__(self):
        return self.doctor_name

    class Meta:
        db_table = 'check_info'
