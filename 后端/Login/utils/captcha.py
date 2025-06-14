import random
import uuid
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.cache import cache


class Captcha:
    def __init__(self):
        self.code_length = 4
        self.cache_key_prefix = "captcha_"
        self.expire_time = 300  # 5分钟过期

    def generate_code(self):
        """生成随机数字验证码"""
        chars = '0123456789abcdefghijklmnopqrstuvwxyjABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return ''.join(random.choice(chars) for _ in range(self.code_length))

    def generate_image(self, code):
        """生成验证码图片"""
        width, height = 120, 40
        image = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # 绘制干扰线
        for _ in range(5):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        # 绘制验证码
        font = ImageFont.truetype('arial.ttf', 24)  # 确保字体文件存在
        for i, char in enumerate(code):
            draw.text((10 + i * 24, 10), char, font=font, fill=(0, 0, 0))

        # 转换为字节流
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        return buffer.getvalue()

    def create_captcha(self):
        """生成验证码并保存到缓存"""
        code = self.generate_code()
        key = self.cache_key_prefix + str(uuid.uuid4())
        cache.set(key, code, self.expire_time)
        image_data = self.generate_image(code)
        return key, image_data


    def validate_captcha(self, key, user_input):
        """
        校验验证码
        """
        cached_code = cache.get(key)
        if not cached_code:
            return False
        cache.delete(key)  # 验证后立即失效
        return cached_code.lower() == user_input.lower()
