from rest_framework.routers import DefaultRouter
from Stockist.views import *
from django.urls import path


router = DefaultRouter()
router.register(r'stockist', StockistViewset)
router.register(r'company-stockist', CompanyStockistViewset,
                basename='company_stockist')
router.register(r'company-stockist-with-out-pagination', CompanyStockistWithoutPaginationViewset,
                basename='company_stockist_without_pagination')
router.register(r'company-stockist-mpo', CompanyMPOStockistViewSet,
                basename='company_mpo_stockist')
urlpatterns = router.urls