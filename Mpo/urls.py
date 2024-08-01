from rest_framework.routers import DefaultRouter
from django.urls import path


from Mpo.views import *


router = DefaultRouter()
# router.register(r'company-mpo', CompanyMpoViewset)
router.register(r'company-divisionwise-mpo', CompanyDivisionwiseMpoViewset)
router.register(r'shift', ShiftViewset)
router.register(r'purpose-of-visit', PurposeofVisitViewset)
router.register(r'working-day', WorkingDaysViewset)
router.register(r'tour-plan', TourPlanViewset)
router.register(r'shift-wise-tour-plan', ShiftWiseTourplanViewset)
router.register(r'company-mpo-tour-plan', CompanyMpoTourplanViewset,basename='company_mpo_tour_plan')
router.register(r'company-mpo-tour-plan-with-out-pagination', 
                CompanyMpoTourplanWithOutPagination, basename='company_mpo_tour_plan_without_pagination')
router.register(r'company-mpo-area', CompanyMPOAreaViewset, basename="company_mpo_area")
# router.register(r'company-mpo-doctor', CompanyMPODoctorViewset, basename='company_mpo_doctor')
urlpatterns = [
        path('working-days/', ActiveWorkingDaysViewset.as_view(), name='working-days'),
        path('tour-plan-bulk-update/', tour_plan_bulk_update_by_month),
        path('get-tourplan-of-30-days/', get_the_mpo_tourplan_of_30_days),
        path('tourplan-same-as-previous-month/', tour_plan_same_as_previous_month),
        path('bulk-create-mpo-tour-plan', bulk_create_mpo_tour_plan),
        path('get-mpo-list', get_mpo_list),
        path('transfer-mpo-data', transfer_mpo_chemist_doctor),
        # path('tourplan-to-select-to-add', get_tour_plan_mpo),
        ]
urlpatterns += router.urls