import json

import oss2
import requests
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.models import patient
from .models import eyeImage, disease, ImagePatientRelation, ImageDiseaseRelation, eyeImageResult
from .serializers import EyeImageSerializer, DiseaseSerializer, EyeImageResultSerializer
from .utils import upload_to_oss
import zipfile
import io
from django.conf import settings

DISEASE_MAPPING = {
    "N": "正常",
    "D": "糖尿病",
    "G": "青光眼",
    "C": "白内障",
    "A": "AMD",
    "H": "高血压",
    "M": "近视",
    "O": "其他疾病"
}

class PredictAPI(APIView):

    def post(self, request, *args, **kwargs):
        patient_id = request.data.get('patient_id')
        patient_name = request.data.get('patient_name')

        if not patient_id or not patient_name:
            return Response({'error': '必须提供患者ID和姓名'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient_ = patient.objects.get(patient_id=patient_id, patientName=patient_name)
        except patient.DoesNotExist:
            return Response({'error': '患者不存在或ID与姓名不匹配'}, status=status.HTTP_404_NOT_FOUND)

        # 获取上传的左右眼图片
        left_eye_file = request.FILES.get('left_eye')  # 左眼图片
        right_eye_file = request.FILES.get('right_eye')  # 右眼图片

        # 验证至少上传一张图片
        if not left_eye_file and not right_eye_file:
            return Response({"error": "At least one file must be uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        left_image_obj = None
        right_image_obj = None
        if left_eye_file:
            left_image_obj = eyeImage.objects.create(image_url=left_eye_file, eye_side='left')
        if right_eye_file:
            right_image_obj = eyeImage.objects.create(image_url=right_eye_file, eye_side='right')

        if left_image_obj:
            ImagePatientRelation.objects.create(patient_id=patient_id, image_id=left_image_obj.image_id)
        if right_image_obj:
            ImagePatientRelation.objects.create(patient_id=patient_id, image_id=right_image_obj.image_id)



        combined_result = {}
        diseases = []
        response_data = {
            "combined_result": None,  # 合并后的 result，只有上传两张图片时会有
            "combined_disease_types": None,  # 合并后解析的疾病类型
            "left_result": None,  # 左眼的 result
            "left_disease_types": None,  # 左眼解析出的疾病类型
            "left_cams": None,  # 左眼热力图
            "right_result": None,  # 右眼的 result
            "right_disease_types": None,  # 右眼解析出的疾病类型
            "right_cams": None  # 右眼热力图
        }

        # 调用外部接口的 URL
        url = "http://192.168.1.197:8000/predict"

        try:
            # 对左眼图片进行预测
            if left_eye_file:
                left_files = {'file': (left_eye_file.name, left_eye_file, left_eye_file.content_type)}
                left_response = requests.post(url, files=left_files)
                if left_response.status_code != 200:
                    return Response({"error": "Failed to predict left eye.", "details": left_response.text}, status=left_response.status_code)
                left_data = left_response.json()
                response_data["left_result"] = left_data.get("result", {})
                response_data["left_disease_types"] = [
                    DISEASE_MAPPING[key] for key, value in left_data.get("result", {}).items() if value == 1
                ]

                response_data["left_cams"] = left_data.get("cams", {})
                eyeImageResult.objects.create(
                    image_id=left_image_obj.image_id,
                    image_result=left_data.get('left_disease_types', ''),
                    image_desc=left_data.get('left_cams', '')
                )

                # 对右眼图片进行预测
            if right_eye_file:
                right_files = {'file': (right_eye_file.name, right_eye_file, right_eye_file.content_type)}
                right_response = requests.post(url, files=right_files)
                if right_response.status_code != 200:
                    return Response({"error": "Failed to predict right eye.", "details": right_response.text}, status=right_response.status_code)
                right_data = right_response.json()
                response_data["right_result"] = right_data.get("result", {})
                response_data["right_disease_types"] = [
                    DISEASE_MAPPING[key] for key, value in right_data.get("result", {}).items() if value == 1
                ]
                response_data["right_cams"] = right_data.get("cams", {})
                eyeImageResult.objects.create(
                    image_id=right_image_obj.image_id,
                    image_result=right_data.get('right_disease_types', ''),
                    image_desc=right_data.get('right_cams', '')
                )

                # 如果上传了两张图片，则合并 result 并解析疾病类型
            if left_eye_file and right_eye_file:
                left_result = response_data["left_result"]
                right_result = response_data["right_result"]

                # 合并 result 字段
                for key in DISEASE_MAPPING.keys():
                    combined_result[key] = max(left_result.get(key, 0), right_result.get(key, 0))

                # 特殊处理：如果最终结果是 "N"（正常），必须左右眼都正常
                if combined_result.get("N") == 1:
                    if left_result.get("N") != 1 or right_result.get("N") != 1:
                        combined_result["N"] = 0

                response_data["combined_result"] = combined_result
                response_data["combined_disease_types"] = [
                    DISEASE_MAPPING[key] for key, value in combined_result.items() if value == 1
                ]
                combined_disease_types = response_data["combined_disease_types"]
                left_cams = response_data.get("left_cams", "")
                right_cams = response_data.get("right_cams", "")
                combined_types_str = ",".join(combined_disease_types)
                eyeImageResult.objects.create(
                    image_id=left_image_obj.image_id,  # 或自定义合并专用ID
                    image_result=combined_types_str,
                    image_desc=json.dumps({
                        "left_heatmap": left_cams,
                        "right_heatmap": right_cams
                    }, ensure_ascii=False)
                )

            return Response(response_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:

            return Response({"error": "External API call failed.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
查询历史记录
"""
class EyeImageHistoryListView(APIView):
    def get(self, request):
        queryset = eyeImageResult.objects.all().order_by('-result_id')
        serializer = EyeImageResultSerializer(queryset, many=True)
        return Response(serializer.data)
"""  
图片上传视图  
"""
class ImageUploadView(APIView):



    def post(self, request, *args, **kwargs):
        patient_id = request.data.get('patient_id')
        patient_name = request.data.get('patient_name')

        if not patient_id or not patient_name:
            return Response({'error': '必须提供患者ID和姓名'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient_ = patient.objects.get(patient_id=patient_id, patientName=patient_name)
        except patient.DoesNotExist:
            return Response({'error': '患者不存在或ID与姓名不匹配'}, status=status.HTTP_404_NOT_FOUND)


        files = request.FILES.getlist('images')
        eye_sides = request.POST.getlist('eye_sides')

        if isinstance(eye_sides, str):
            eye_sides = eye_sides.split(',')


        if not files:
            return Response({'error': '该文件不存在'}, status=status.HTTP_400_BAD_REQUEST)
        if len(files) != len(eye_sides):
            return Response({'error': "选择左右眼的数量必须与上传的图像数量相匹配。"}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_images = []
        relations = []

        try:
            for file, eye_side in zip(files, eye_sides):

                if eye_side not in ['left', 'right']:
                    return Response({'error': "选择左右眼的格式必须为'left'或者'right'"}, status=status.HTTP_400_BAD_REQUEST)

                file_path = f"uploads/{eye_side}/{file.name}"
                file_url = upload_to_oss(file, file_path)

                image_result, image_desc = self.generate_image_analysis(file_url)


                image = eyeImage.objects.create(
                    eye_side=eye_side,
                    image_url=file_url,
                    image_result=image_result,
                    image_desc=image_desc
                )


                serializer = EyeImageSerializer(image)
                uploaded_images.append(serializer.data)

                relations.append(ImagePatientRelation(patient_id=patient_id, image_id=image.image_id))
            ImagePatientRelation.objects.bulk_create(relations)
            relations_data = [
                {'patient_id': relation.patient_id, 'image_id': relation.image_id}
                for relation in relations
            ]

            return Response({'uploaded_images': uploaded_images, 'relations': relations_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def generate_image_analysis(self, file_url):

        image_result = "Normal"
        image_desc = "这是一段描述"


        return image_result, image_desc



"""
图片详情视图
"""
class ImageDetailView(APIView):


    def get(self, request, *args, **kwargs):
        image_list = eyeImage.objects.all()
        serializer = EyeImageSerializer(instance=image_list, many=True)
        return Response({'msg':'获取成功',
                            'data':serializer.data
                         }, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        image_id = request.data.get('image_id')
        try:
            images = eyeImage.objects.get(image_id=image_id)

            serializer = EyeImageSerializer(images)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except eyeImage.DoesNotExist:
            return Response({'error': '未找到图片'}, status=status.HTTP_404_NOT_FOUND)


"""
批量下载图片，返回 ZIP 文件
"""

class MultiImageDownloadView(APIView):


    def post(self, request, *args, **kwargs):

        image_ids = request.data.get('image_ids', [])
        if not image_ids:
            return Response({'error':'未找到图片'}, status=status.HTTP_400_BAD_REQUEST)


        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for image_id in image_ids:
                try:

                    images = eyeImage.objects.get(image_id=image_id)
                    object_key = images.image_url.replace(
                        settings.ALIYUN_OSS_CONFIG['BUCKET_URL'] + '/', ''
                    )

                    auth = oss2.Auth(
                        settings.ALIYUN_OSS_CONFIG['ACCESS_KEY_ID'],
                        settings.ALIYUN_OSS_CONFIG['ACCESS_KEY_SECRET']
                    )
                    bucket = oss2.Bucket(
                        auth,
                        settings.ALIYUN_OSS_CONFIG['ENDPOINT'],
                        settings.ALIYUN_OSS_CONFIG['BUCKET_NAME']
                    )


                    result = bucket.get_object(object_key)
                    file_name = object_key.split('/')[-1]
                    zip_file.writestr(file_name, result.read())
                except eyeImage.DoesNotExist:

                    return Response({
                        'error': f"未找到图片ID为{image_id}的图片"
                    }, status=status.HTTP_404_NOT_FOUND)
                    continue

                except Exception as e:

                    return Response({
                        'error': f"下载图片ID为{image_id}的图片时出错: {str(e)}"
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    continue
        zip_buffer.seek(0)

        return HttpResponse(
            zip_buffer,
            content_type='application/zip',
            headers={
                'Content-Disposition': 'attachment; filename="images.zip"'
            }
        )

class DiseaseInfoView(APIView):

    """
    获取疾病信息，以及疾病对应的患者和患者的疾病图片
    """
    def get(self, request, *args, **kwargs):
        diseases = disease.objects.all()
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data)
    def post(self, request, *args, **kwargs):

        patient_name = request.data.get('name')
        if not patient_name:
            return Response({"error": "患者名称不能为空"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            patient_obj = patient.objects.get(patientName=patient_name)
        except patient.DoesNotExist:
            return Response({"error": "未找到该患者"}, status=status.HTTP_404_NOT_FOUND)



        image_patient_relations = ImagePatientRelation.objects.filter(patient_id=patient_obj.patient_id)
        if not image_patient_relations.exists():
            return Response({"error": "未找到与该病人相关的影像信息"}, status=status.HTTP_404_NOT_FOUND)

        image_ids = [relation.image_id for relation in image_patient_relations]
        if not image_ids:
            return Response({"error": "未找到与该病人相关的影像信息"}, status=status.HTTP_404_NOT_FOUND)


        image_disease_relations = ImageDiseaseRelation.objects.filter(image_id__in=image_ids)
        #print(image_disease_relations)
        #print(image_patient_relations.values('image_id'))
        print(image_disease_relations.values('disease_id'))

        #image_disease_relations = ImageDiseaseRelation.objects.filter(image_id=image_ids)
        if not image_disease_relations.exists():
            return Response({"error": "未找到与该病人相关的疾病信息"}, status=status.HTTP_404_NOT_FOUND)

        disease_ids = [int(relation.disease_id) for relation in image_disease_relations]
        if not disease_ids:
            return Response({"error": "未找到与该病人相关的疾病信息"}, status=status.HTTP_404_NOT_FOUND)

        print(f"Disease IDs: {disease_ids}")
        diseases = disease.objects.filter(disease_id__in=disease_ids)
        #diseases = disease.objects.filter(disease_id=disease_ids)
        print(diseases)
        print(f"Image IDs: {image_ids}")


        serializer = DiseaseSerializer(diseases, many=True)
        serialized_data = serializer.data

        print(serializer.data)


        return Response({
            "patient_id": patient_obj.patient_id,
            "patient_name": patient_obj.patientName,
            "diseases": serialized_data
        }, status=status.HTTP_200_OK)