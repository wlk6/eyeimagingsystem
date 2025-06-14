from rest_framework import serializers

from user.models import patient, DoctorPatientRelation


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = patient
        fields = '__all__'


class DoctorPatientRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorPatientRelation
        fields ='__all__'