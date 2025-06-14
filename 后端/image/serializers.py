from rest_framework import serializers

from user.models import patient
from .models import eyeImage, disease, ImageDiseaseRelation, ImagePatientRelation, eyeImageResult


class EyeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = eyeImage
        fields = '__all__'

class EyeImageResultSerializer(serializers.ModelSerializer):
    image_info = serializers.SerializerMethodField()

    class Meta:
        model = eyeImageResult
        fields = ['result_id', 'image_id', 'image_result', 'image_desc', 'image_info']

    def get_image_info(self, obj):
        try:
            image = eyeImage.objects.get(image_id=obj.image_id)
            return EyeImageSerializer(image).data
        except eyeImage.DoesNotExist:
            return None
class DiseaseSerializer(serializers.ModelSerializer):
    patients = serializers.SerializerMethodField()
    class Meta:
        model = disease
        fields = '__all__'

    def get_patients(self, obj):
        # 获取与疾病相关的患者和图片
        image_disease_relations = ImageDiseaseRelation.objects.filter(disease_id=obj.disease_id)
        patient_data = []

        for relation in image_disease_relations:

            image_id = relation.image_id
            image_patient_relations = ImagePatientRelation.objects.filter(image_id=image_id)

            for image_patient_relation in image_patient_relations:
                # 获取患者信息
                patient_ = patient.objects.get(patient_id=image_patient_relation.patient_id)
                # 获取图像信息
                image = eyeImage.objects.get(image_id=image_patient_relation.image_id)
                patient_data.append({
                    'patient_id': patient_.patient_id,
                    'patient_name': patient_.patientName,
                    'image_id': image.image_id,
                    'image_url': image.image_url,
                    'image_desc': image.image_desc,
                    'image_result': image.image_result,
                    'eye_side': image.eye_side,
                    'image_date': image.image_date
                })

        return patient_data

class ImagePatientRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePatientRelation
        fields = '__all__'