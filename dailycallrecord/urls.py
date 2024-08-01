from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path
from dailycallrecord import views


router = DefaultRouter()
router.register(r'rewards', RewardViewset)
router.register(r'dcr-for-doctor', DcrForDoctorViewset)
router.register(r'shift-wise-dcr-for-doctor',
                ShiftwiseDcrForDoctorViewset)
router.register(r'mpo-shift-wise-dcr-for-doctor',
                MpoWiseShiftWiseDcrForDoctorViewset,
                basename="mpo_shift_wise_dcr_for_doctor")
router.register(r'mpo-shift-wise-dcr-for-doctor-with-out-pagination',
                MpoWiseShiftWiseDcrForDoctorWithOutPaginationViewset,
                basename="mpo_shift_wise_dcr_for_doctor_with_out_pagination")
router.register(r'dcr-for-doctor-rewards-map',
                DcrForDoctorRewardsMapViewset)
router.register(r'dcr-for-doctor-company-product-map',
                DcrForDoctorCompanyProductMapViewset)
router.register(r'dcr-for-doctor-company-roles-map',
                DcrForDoctorCompanyRolesMapViewset)
router.register(r'dcr-for-doctor-product-reward-role',
                DCRProductRewardsRolesViewset,
                basename="dcr_for_doctor_product_reward_role")
router.register(r'chemist-ordered-product',
                ChemistOrderedProductViewset)
router.register(r'dcr-for-chemist', DcrForChemsitViewset)
router.register(r'shift-wise-dcr-for-chemist',
                ShiftwiseDcrForChemistViewset)
router.register(r'mpo-shift-wise-dcr-for-chemist',
                MpoWiseShiftWiseDcrForChemistViewset)
router.register(r'dcr-for-chemist-product',
                DcrForChemistProductViewset)
router.register(r'dcr-for-chemist-company-product-map',
                DcrForChemistPromotedProductMapViewset)
router.register(r'dcr-for-chemist-rewards-map',
                DcrForChemistRewardsMapViewset)
router.register(r'dcr-for-chemist-company-roles-map',
                DcrForChemistCompanyRolesMapViewset)
router.register(r'dcr-for-chemist-product-rewards-roles',
                DCRChemistProductRewardsRolesViewset,
                basename='dcr_for_chemist_product_rewards_roles')
router.register(r'dcr-for-chemist-ordered-product-information',
                DCRChemistOrderedProductInformationViewset,
                basename='dcr_for_chemist_ordered_product_information')
router.register(r'stockist-ordered-product',
                StockistOrderedProductViewset)            
router.register(r'dcr-for-stockist', DcrForStockistViewset)
router.register(r'shift-wise-dcr-for-stockist',
                ShiftwiseDcrForStockistViewset)
router.register(r'mpo-shift-wise-dcr-for-stockist',
                MpoWiseShiftWiseDcrForStockistViewset)
router.register(r'dcr-for-stockist-ordered-product',
               DcrForStockistOrderedProductViewset)
# router.register(r'dcr-for-stockist-product-map',
#                 DcrForStockistProductMapViewset)
router.register(r'dcr-for-stockist-rewards-map',
                DcrForStockistRewardsMapViewset)
router.register(r'dcr-for-stockist-company-roles-map',
                DcrForStockistCompanyRolesMapViewset)
router.register(r'dcr-for-stockist-product-rewards-roles',
                DCRStockistProductRewardsRolesViewset,
                basename='dcr_for_stockist_product_rewards_roles')

urlpatterns = [
    path('graph/', views.get_maximum_ordered_product_by_chemist_and_stockist)
]
urlpatterns += router.urls