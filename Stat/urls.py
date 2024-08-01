from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter

from Stat.views import (
    CompanyDCRTourPlanValidityViewsets,
    MPOMissedCallModelViewsets,
    get_mpo_data,
    get_higher_order_data)


router = DefaultRouter()

router.register(
    r'tour-plan-validity',
    CompanyDCRTourPlanValidityViewsets,
    basename="tour_plan_validity")
router.register(
    r'mpo-missed-call',
    MPOMissedCallModelViewsets,
    basename="mpo_missed_call"
)

urlpatterns = [
    path('get-stat/', get_stat),
    path('get-missed-call-data/', get_missed_call_data),
    path('get-mpo-data/', get_mpo_data),
    path('get-higher-order-data/', get_higher_order_data)

]

urlpatterns += router.urls