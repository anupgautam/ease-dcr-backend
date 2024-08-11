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
    CompanyHolidayDateViewset,
    CompanyRolesTPLockViewset
)


router = DefaultRouter()
router.register(r"company", CompanyViewset, basename="company")
router.register(r"division", DivisionViewset, basename="division")
router.register(r"roles", RolesViewset, basename="roles")
router.register(r"notices", NoticesViewset, basename="notice")
# router.register(r'working-area', WorkingAreaViewset)
# router.register(r'working-area', WorkingAreaViewset)
router.register(r"working-hour", WorkingHourViewset, basename="working_hour")
router.register(r"company-wise-division", CompanyWiseDivsionViewset, basename="company_wise_division")
router.register(r"company-area", CompanyAreaViewset, basename="company_area")
router.register(
    r"company-area-without-to-representation",
    CompanyAreaViewsetWithoutToRepresentation,
    basename="company_area_without_to_representation",
)
router.register(r"company-working-hour", CompanyWorkingHourViewset, basename="company_working_hour")
router.register(r"company-roles", CompanyRolesViewset, basename="company_roles")
router.register(r"company-notice", CompanyNoticesViewset, basename="company_notice")
router.register(r"add-notices", NoticeViewset, basename="add_notices")
router.register(r"company-roles-salary", CompanyRolesSalaryViewset, basename="company_roles_salary")
router.register(r"company-holiday", CompanyHolidayViewset, basename="company_holiday")
router.register(r"company-holiday-area", CompanyHolidayAreaViewset, basename="company_holiday_area")
router.register(r"company-holiday-date", CompanyHolidayDateViewset, basename="company_holiday_date")
router.register(r"company-roles-tp-lock", CompanyRolesTPLockViewset, basename="company_roles_tp_lock")
urlpatterns = router.urls
