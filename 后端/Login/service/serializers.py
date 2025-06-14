import re


from rest_framework import serializers

from Login.models import doctor, checkInfo
from Login.utils import encrpty
from Login.utils.captcha import Captcha


class addDoctorSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=64, write_only=True)

    class Meta:
        model = doctor
        fields = ['doctor_id', 'doctor_name', 'password', 'password_confirm', 'position', 'gender']

    def validate_password(self, data):
        if not data:
            raise serializers.ValidationError('请输入密码')
        return encrpty.md5(data)

    def validate_password_confirm(self, data):
        if not data:
            raise serializers.ValidationError("请确定密码")
        password = self.initial_data.get("password")
        if password != data:
            raise serializers.ValidationError("两次密码输入不一致，请重新输入")
        return encrpty.md5(data)

    def validate(self, data):
        data.pop('password_confirm')
        return data


class getDoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctor
        exclude = ['password']


positions = [
    ('chief_physician', '主任医师'),
    ('associate_physician', '副主任医师'),
    ('attending_doctor', '主治医师')
]


# 医生提交修改信息申请
class doctorAlterInfoSerializer(serializers.ModelSerializer):
    # 修改字段为选填
    doctor_name = serializers.CharField(required=False, max_length=50)
    gender = serializers.CharField(required=False, max_length=6)
    phone = serializers.CharField(required=False, max_length=15)
    position = serializers.ChoiceField(required=False, choices=positions)
    email = serializers.EmailField(required=False, max_length=50)
    avatar = serializers.ImageField(required=False)
    introduce = serializers.CharField(required=False, max_length=1000)
    captcha_key = serializers.CharField(write_only=True)
    captcha_code = serializers.CharField(write_only=True)

    class Meta:
        model = checkInfo
        fields = ['doctor_id', 'doctor_name', 'gender', 'email', 'phone', 'position', 'avatar', 'introduce',
                  'captcha_key',
                  'captcha_code', 'is_password', 'result', 'alter_time']

    def validate_email(self, value):
        pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not re.match(pattern, value):
            raise serializers.ValidationError("该邮箱格式错误，请确定格式正常后重新输入")
        if doctor.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被注册')
        return value

    def validate_phone(self, value):
        pattern = re.compile(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$')
        if not re.match(pattern, value):
            raise serializers.ValidationError("该手机号码格式错误，请确定格式正确后重新输入")
        if doctor.objects.filter(phone=value).exists():
            raise serializers.ValidationError("该手机号已被注册")
        return value

    def validate_captcha_code(self, data):
        key = self.initial_data.get("captcha_key")
        captcha = Captcha()
        check = captcha.validate_captcha(key, data)
        if check is True:
            return data
        raise serializers.ValidationError(check)

    def validate(self, data):
        data.pop('captcha_key')
        data.pop('captcha_code')
        return data


# 管理员获取待审核医生信息
class checkInfoSerializer(serializers.ModelSerializer):
    check_info_id = serializers.IntegerField()

    class Meta:
        model = checkInfo
        fields = ['check_info_id', 'doctor_id', 'doctor_name', 'gender', 'email', 'phone', 'position', 'avatar',
                  'introduce',
                  'alter_time']


# 管理员给出审核信息结果
class afterCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = checkInfo
        fields = "__all__"


# 医生提交修改密码申请
class alterPasswordSerializer(serializers.ModelSerializer):
    password_verify = serializers.CharField(write_only=True)  # 辅助字段，不保存到数据库
    captcha_key = serializers.CharField(write_only=True)
    captcha_code = serializers.CharField(write_only=True)

    class Meta:
        model = checkInfo
        fields = ['doctor_id', 'password', 'password_verify', 'captcha_key', 'captcha_code', 'is_password', 'result',
                  'alter_time']

    def validate(self, data):
        doctor_id = data.get('doctor_id')
        if not doctor_id:
            return serializers.ValidationError("ID账号不能为空")
        # 密码一致性校验
        if data['password'] != data['password_verify']:
            raise serializers.ValidationError("两次密码输入不一致")
        # 验证码校验
        captcha = Captcha()
        if not captcha.validate_captcha(data['captcha_key'], data['captcha_code']):
            raise serializers.ValidationError("验证码错误或已过期")
        doctor_instance = doctor.objects.filter(doctor_id=doctor_id).first()
        if not doctor_instance:
            return serializers.ValidationError("用户不存在")

        # 清理字段
        data.pop('password_verify')
        data.pop('captcha_key')
        data.pop('captcha_code')

        # 密码加密
        data['password'] = encrpty.md5(data['password'])
        return data

    def update(self, instance, validated_data):
        instance.is_password = validated_data.get('is_password', instance.is_password)
        instance.alter_time = validated_data.get('alter_time', instance.alter_time)
        instance.result = validated_data.get('result', instance.result)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class afterCheckPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = checkInfo
        fields = ['check_info_id', 'doctor_id', 'password', 'result', 'advice', 'check_time']


class checkPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = checkInfo
        fields = ['check_info_id', 'doctor_id', 'alter_time']


class getDorctorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctor
        exclude = ['password']
