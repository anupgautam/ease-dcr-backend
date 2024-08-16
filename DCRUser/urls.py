from rest_framework.routers import DefaultRouter
from DCRUser.views import (UserViewset,
                        CompanyUserViewset,
                        CompanyUserRoleViewset,
                        CompanyUserRoleViewsetWithoutPagination,
                        CompanyUserWithoutPagination,
                        CompanyUserAttendanceViewset,
                        get_upper_company_user_from_company_name_and_role_name,
                        get_executives_from_user_id,
                        get_all_the_upper_level_users_from_company_user_role_id,
                        get_all_the_lower_level_users_from_company_user_role_id,
                        get_user_hierarchy,
                        get_admin_user_id,
                        # make_user_present
                        )
from django.urls import path


router = DefaultRouter()
# router.register(r'user', UserViewset)
router.register(r'company-user', CompanyUserViewset,
                basename='company_user')
router.register(r'company-user-without-pagination', CompanyUserWithoutPagination,
                basename='company_user_without_pagination')
router.register(r'company-user-role', CompanyUserRoleViewset,
                basename='company_user_role')
router.register(r'company-user-role-without-pagination', CompanyUserRoleViewsetWithoutPagination,
                basename="company_user_role_without_pagination")
router.register(r'company-user-attendance', CompanyUserAttendanceViewset,
                basename="company_user_attendance")
urlpatterns = [
    path('get-upper-level-user-from-company-role/',get_upper_company_user_from_company_name_and_role_name),
    path('get-all-upper-level-user-from-company-user-role/',get_all_the_upper_level_users_from_company_user_role_id),
    path('get-executives-from-user-id/',get_executives_from_user_id),
    path('get-all-lower-level-users-from-company-user-role-id/',get_all_the_lower_level_users_from_company_user_role_id),
    path('get-user-hierarchy/',get_user_hierarchy),
    path('get-admin-id/',get_admin_user_id),
    # path('make-user-present/',make_user_present),
]
urlpatterns += router.urls
