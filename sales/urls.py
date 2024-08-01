from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter

from sales.views import SecondarySalesViewsets, PrimarySalesViewsets


router = DefaultRouter()

router.register(
    r'secondary-sales',
    SecondarySalesViewsets,
    basename="secondary_sales"),
router.register(
    r'primary-sales',
    PrimarySalesViewsets,
    basename="primary_sales"
)

urlpatterns = [
]

urlpatterns += router.urls