from rest_framework.routers import DefaultRouter
from Product.views import *
from django.urls import path

router = DefaultRouter()
router.register(r'product', ProductViewset)
router.register(r'company-product', CompanyProductviewset,
                basename='company_product')
router.register(r'company-product-without-pagination',
                CompanyProductWithoutPaginationviewset,
                basename='company_product_without_pagination')
router.register(r'company-division-product', CompanyDivisionProductViewset,
                basename="company_division_product")
router.register(r'company-division-product-without-pagination',
                CompanyDivissionProductWithoutPagination)
urlpatterns = [
    path(r'get-chemist-ordered-product/', get_all_ordered_product_of_chemist),
    path(r'get-stockist-ordered-product/', get_stockist_ordered_product)
]
urlpatterns += router.urls