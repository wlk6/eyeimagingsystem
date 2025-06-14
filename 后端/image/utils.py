import oss2
from django.conf import settings

"""
    上传文件到阿里云 OSS
    :param file: 文件对象
    :param file_path: OSS 中的文件路径
    :return: 文件的完整 URL
"""
def upload_to_oss(file, file_path):

    config = settings.ALIYUN_OSS_CONFIG
    auth = oss2.Auth(config['ACCESS_KEY_ID'], config['ACCESS_KEY_SECRET'])
    bucket = oss2.Bucket(auth, config['ENDPOINT'], config['BUCKET_NAME'])

    # 上传文件到 OSS
    bucket.put_object(file_path, file)

    # 返回文件的完整 URL
    return f"{config['BUCKET_URL']}/{file_path}"


