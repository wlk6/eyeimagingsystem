"""
URL configuration for medical_imaging project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from rest_framework.documentation import include_docs_urls

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView, TokenVerifyView,
# )


urlpatterns = [
    # path('docs/', include_docs_urls(title='测试平台接口文档', description='xxx接口文档')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('image/', include('image.urls')),
    path('Login/',include('Login.urls')),

]
