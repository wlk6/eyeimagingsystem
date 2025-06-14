from django.db import models

eye_side = [
    (1, "left"),
    (2, "right")
]

class eyeImageResult(models.Model):
    result_id = models.AutoField(primary_key=True)

    image_id = models.IntegerField()

    image_result = models.CharField(max_length=15)  # 图像的诊断结果
    image_desc = models.TextField()  # 图像base64编码

    def __str__(self):
        return self.result_id
    class Meta:
        db_table = 'image_result'
class eyeImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    eye_side = models.CharField(max_length=6, choices=eye_side)  # 哪边眼睛
    image_date = models.DateTimeField(auto_now_add=True)  # 图像上传日期
    image_type = models.CharField(max_length=10)  # 图像类型
    image_url = models.URLField()  # 存储图片的 OSS URL
    image_result = models.CharField(max_length=15)  # 图像的诊断结果
    image_desc = models.TextField()  # 图像诊断描述

    def __str__(self):
        return self.image_id

    class Meta:
        db_table = 'image'


class disease(models.Model):
    disease_id = models.AutoField(primary_key=True)
    disease_name = models.CharField(max_length=15)
    disease_desc = models.TextField()
    def __str__(self):
        return self.disease_name

    class Meta:
        db_table = 'disease'


class ImagePatientRelation(models.Model):
    """
    影像-患者关系模型
    """
    image_patient_id = models.AutoField(primary_key=True)
    image_id = models.IntegerField(db_column='image_id')
    patient_id = models.IntegerField(db_column='patient_id')
    class Meta:
        db_table = 'image_patient'
        verbose_name = "Image-Patient Relation"
        verbose_name_plural = "Image-Patient Relations"

    def __str__(self):
        return f"Image ID: {self.image_id}, Patient ID: {self.patient_id}"


class ImageDiseaseRelation(models.Model):
    """
    影像-疾病关系模型
    """
    image_disease_id = models.AutoField(primary_key=True)
    image_id = models.IntegerField(db_column='image_id')
    disease_id = models.IntegerField(db_column='disease_id')
    class Meta:
        db_table = 'image_disease'
        verbose_name = "Image-Disease Relation"
        verbose_name_plural = "Image-Disease Relations"

    def __str__(self):
        return f"Image ID: {self.image_id}, Patient ID: {self.disease_id}"