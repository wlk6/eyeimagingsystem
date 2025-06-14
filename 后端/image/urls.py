from django.urls import path
from .views import ImageUploadView, MultiImageDownloadView, ImageDetailView, DiseaseInfoView, PredictAPI, \
    EyeImageHistoryListView

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='upload'),
    path('download/', MultiImageDownloadView.as_view(), name='download'),
    path('detail/', ImageDetailView.as_view(), name='detail'),
    path('disease/', DiseaseInfoView.as_view(), name='disease'),
    path('predict/', PredictAPI.as_view(), name='predict'),
    path('history/', EyeImageHistoryListView.as_view(), name='history'),

]