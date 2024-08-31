from rest_framework.routers import DefaultRouter
from django.urls import path

from Doctors.views import CompanyWiseDoctorViewset
from Doctors.views import *

urlpatterns = [
    # path('combined', CombinedView.as_view())
]
router = DefaultRouter()
router.register(r'doctor', DoctorViewset)
router.register(r'company-wise-doctor-specialization', CompanyDoctorSpecializationViewset)
router.register(r'company-wise-doctor', CompanyWiseDoctorViewset,
                basename='company-wise-doctor')
router.register(r'company-wise-doctor-without-pagination', 
                CompanyWiseDoctorWithOutPagination,
                basename='company_wise_doctor_without_pagination')
router.register(r'doctor-events', DoctorEventsViewset,
                basename='doctor_events')
router.register(r'doctor-events-without-pagination', 
                DoctorEventsViewsetWithOutPagination,
                basename='doctor_events_without_pagination')
urlpatterns += router.urls