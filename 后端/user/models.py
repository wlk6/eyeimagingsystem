from django.contrib.auth import get_user_model
from django.db import models




# Create your models here.
class patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patientName = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=6, blank=True, null=True, default="")
    birthday = models.DateField()
    record = models.TextField()

    def __str__(self):
        return self.patientName

    class Meta:
        db_table = 'patient'


class DoctorPatientRelation(models.Model):
    """
    医生-患者关系模型
    """
    doctor_patient_id = models.AutoField(primary_key=True)
    doctor_id = models.IntegerField(db_column='doctor_id')
    patient_id = models.IntegerField(db_column='patient_id')
    class Meta:
        db_table = 'doctor_patient'  # 映射到数据库中的表名
        verbose_name = "Doctor-Patient Relation"
        verbose_name_plural = "Doctor-Patient Relations"

    def __str__(self):
        return f"Doctor ID: {self.doctor_id}, Patient ID: {self.patient_id}"