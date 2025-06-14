from django.urls import path

from Login import views

urlpatterns = [
    path('doctorLoginView/', views.doctorLoginView.as_view(), name='doctorLoginView'),
    path('adminLoginView/', views.adminLoginView.as_view(), name='adminLoginView'),
    path('ImageCodeView/', views.ImageCodeView.as_view(), name='ImageCodeView'),
    path('getDoctorIdView/', views.GetDoctorIdView.as_view(), name='getDoctorIdView'),
    path('alterPasswordView/', views.alterPasswordView.as_view(), name='alterPasswordView'),
    path('checkPasswordView/', views.checkPasswordView.as_view(), name='checkPasswordView'),
    path('adminGivePasswordCheckAdvice/', views.adminGivePasswordCheckAdvice.as_view(), name='adminGivePasswordCheckAdvice'),
]