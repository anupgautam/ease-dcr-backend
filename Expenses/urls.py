from rest_framework.routers import DefaultRouter
from Expenses.views import *
from django.urls import path, include


router = DefaultRouter()
router.register(r'expenses-type', ExpensesTypeViewset)
router.register(r'company-area-wise-expenses', CompanyAreaWiseExpensesViewset)
router.register(r'leave-application', LeaveApplicationViewset)
router.register(r'mpo-leave-application', MpoWiseLeaveApplicationViewset)
router.register(r'target', TargetViewset)
router.register(r'uploads', UploadsViewset)
router.register(r'expenses', ExpensesViewset)
urlpatterns = [
    path('get-user-expenses/', expenses),
    path('get-whole-year-expenses/', get_whole_year_expenses),
    path('get-target-of-user/', get_target_of_user),
    path('get-detailed-expenses/', get_detailed_expenses),
    path('get-leave-user/', get_leave_user),
    path('get-leave-user-according-to-role/', get_leave_user_according_to_role),
    path('get-leave-user-according-to-executives/', get_leave_user_according_to_executive_level),
    path('get-company-sales/', get_company_sales)
]
urlpatterns += router.urls