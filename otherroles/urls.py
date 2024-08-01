from .views import (
    HigherOrderTourplanViewset,
    HigherOrderDcrViewset,
    HigherOrderTourplanViewsetWithPagination,
    HigherOrderDcrWithPagination,
    get_the_other_roles_tourplan_of_30_days,
    tour_plan_bulk_update_by_month)
from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'higher-order-tour-plan', HigherOrderTourplanViewset,
                basename='higher_order_tourplan')
router.register(r'higher-order-tourplan-with-pagination', HigherOrderTourplanViewsetWithPagination,
                basename='higher_order_tourplan_with_pagination')
router.register(r'higher-order-dcr', HigherOrderDcrViewset,basename='higher_order_dcr')
router.register(r'higher-order-dcr-with-pagination', HigherOrderDcrWithPagination,
                basename='higher_order_dcr_with_pagination')
urlpatterns = [
        path('get-other-roles-tourplan-of-30-days/',get_the_other_roles_tourplan_of_30_days),
        path('higher-order-tour-plan-bulk-update', tour_plan_bulk_update_by_month)
        ]
urlpatterns += router.urls