from rest_framework.routers import DefaultRouter
from Chemist.views import (
    ChemistCategoryViewSet,
    ChemistCompanyAreaViewset,
    ChemistViewSet,
    ChemistWorkingAreaViewset,
    CompanyChemistCategoryViewset,
    CompanyWiseChemistViewSet,
    CompanyWiseChemistWithoutPagination)


router = DefaultRouter()

router.register(r'chemist', ChemistViewSet)
router.register(r'chemist-category', ChemistCategoryViewSet)
router.register(r'company-wise-chemist-category', CompanyChemistCategoryViewset)
router.register(r'company-wise-chemist', CompanyWiseChemistViewSet,
                basename='company_wise_chemist')
router.register(r'company-wise-chemist-with-out-pagination',
                CompanyWiseChemistWithoutPagination,
                basename='company_wise_chemist_with_out_pagination'
                )
router.register(r'chemist-working-area', ChemistWorkingAreaViewset)
router.register(r'company-wise-chemist-working-area', ChemistCompanyAreaViewset)

urlpatterns=router.urls
