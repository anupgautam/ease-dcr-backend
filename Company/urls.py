from rest_framework.routers import DefaultRouter
from Company.views import (
    CompanyViewset,
    DivisionViewset,
    RolesViewset,
    NoticesViewset,
    WorkingHourViewset,
    CompanyWiseDivsionViewset,
    CompanyAreaViewset,
    CompanyAreaViewsetWithoutToRepresentation,
    CompanyWorkingHourViewset,
    CompanyRolesViewset,
    CompanyNoticesViewset,
    NoticeViewset,
    CompanyRolesSalaryViewset,
    CompanyHolidayViewset,
    CompanyHolidayAreaViewset,
)


router = DefaultRouter()
router.register(r"company", CompanyViewset)
router.register(r"division", DivisionViewset)
router.register(r"roles", RolesViewset)
router.register(r"notices", NoticesViewset, basename="notice")
# router.register(r'working-area', WorkingAreaViewset)
# router.register(r'working-area', WorkingAreaViewset)
router.register(r"working-hour", WorkingHourViewset)
router.register(r"company-wise-division", CompanyWiseDivsionViewset)
router.register(r"company-area", CompanyAreaViewset, basename="company_area")
router.register(
    r"company-area-without-to-representation",
    CompanyAreaViewsetWithoutToRepresentation,
    basename="company_area_without_to_representation",
)
router.register(r"company-working-hour", CompanyWorkingHourViewset)
router.register(r"company-roles", CompanyRolesViewset)
router.register(r"company-notice", CompanyNoticesViewset)
router.register(r"add-notices", NoticeViewset)
router.register(r"company-roles-salary", CompanyRolesSalaryViewset)
router.register(r"company-holiday", CompanyHolidayViewset)
router.register(r"company-holiday-area", CompanyHolidayAreaViewset)
urlpatterns = router.urls
