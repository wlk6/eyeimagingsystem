from django.conf.urls.static import static
from django.urls import path

from medical_imaging import settings
from user.views import adminGetCheckList, adminCheckDoctorInfo, adminGiveCheckAdvice, getDoctorInfo, getDoctorListView, selectDoctor
from user.views import adminDelDoctorAccount, adminAddDoctorAccount, doctorAlterInfo, PatientView, PatientDetailView

urlpatterns = [
    path('adminDelDoctorAccount/', adminDelDoctorAccount.as_view(),name='adminDelDoctorAccount'),
    path('adminAddDoctorAccount/', adminAddDoctorAccount.as_view(),name='adminAddDoctorAccount'),
    path('doctorAlterInfo/', doctorAlterInfo.as_view(), name='doctorAlterInfo'),
    path('adminGetCheckList/', adminGetCheckList.as_view(), name='adminGetCheckList'),
    path('adminCheckDoctorInfo/', adminCheckDoctorInfo.as_view(), name='adminCheckDoctorInfo'),
    path('adminGiveCheckAdvice/', adminGiveCheckAdvice.as_view(), name='adminGiveCheckAdvice'),
    # path('detail/',PatientView.as_view(),name='detail'),
    path('detail/',PatientView.as_view(),name='detail'),
    # path('print/',DebugView.as_view(),name='print'),
    path('selectAndUpdate/',PatientDetailView.as_view(),name='selectAndUpdate'),
    path('getDoctorInfo/', getDoctorInfo.as_view(), name='getDoctorInfo'),
    path('getDoctorListView/', getDoctorListView.as_view(), name='getDoctorListView'),
    path('selectDoctor/', selectDoctor.as_view(), name='selectDoctor'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
