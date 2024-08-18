from django.db import models
from Company.models import (
    Company,
    CompanyArea,
    CompanyRoles
    )
from DCRUser.models import CompanyUserRole
from Mpo.models import CompanyMpoTourPlan
from otherroles.models import HigherOrderTourplan
from bsdate.fields import BSDateField



class TimeStamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


# This model stores the type of expenses
class ExpensesType(TimeStamp, models.Model):
    expenses_type = models.CharField(max_length=500)


# This model stores the expenes rate of the company according to
# company
class CompanyAreaWiseExpeneses(TimeStamp, models.Model):
    company_name = models.ForeignKey(Company, 
        on_delete=models.CASCADE)
    area_name = models.ForeignKey(CompanyArea,
        on_delete=models.CASCADE)
    expenses_rate = models.DecimalField(max_digits=10,
    decimal_places=6) 

STATUS = (
    ("pending", "pending"),
    ("approved", "approved"),
    ("rejected", "rejected"),
)

# This model is used to store the application of the mpo
class LeaveApplication(models.Model):
    leave_type = models.CharField(max_length=200)
    leave_cause = models.TextField()
    leave_from = BSDateField()
    leave_to = BSDateField()
    leave_status = models.CharField(
        max_length = 20,
        choices = STATUS,
        default = 'pending')
    is_submitted = models.BooleanField(default=False)
    submission_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(CompanyUserRole,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)
    submit_to = models.ForeignKey(CompanyUserRole,
                                  on_delete=models.CASCADE,
                                  related_name='submit_to',
                                  blank=True,
                                  null=True)
    
class MpoWiseLeaveApplication(models.Model):
    mpo_name = models.ForeignKey(CompanyUserRole,
                                 on_delete=models.CASCADE)
    application_id = models.ForeignKey(LeaveApplication,
                                       on_delete=models.CASCADE)
    

class Target(models.Model):
    year = models.CharField(max_length=4,
                            blank=True,
                            null=True)
    target_from = models.ForeignKey(CompanyUserRole,
                                    on_delete=models.CASCADE,
                                    related_name='target_from',
                                    blank=True,
                                    null=True)
    target_to = models.ForeignKey(CompanyUserRole,
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True,
                                  related_name='target_to')
    target_amount = models.DecimalField(max_digits=10,
                                        decimal_places=1,
                                        blank=True,
                                        null=True)
    sales = models.DecimalField(max_digits=10,
                                decimal_places=1,
                                blank=True,
                                null=True)


class Uploads(TimeStamp, models.Model):
    mpo_name = models.ForeignKey(CompanyUserRole,
                                 on_delete=models.CASCADE)
    upload_type = models.CharField(max_length=20)
    upload_name = models.CharField(max_length=200)
    upload = models.FileField(upload_to='uploads/')
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)


class ExpenseData(TimeStamp, models.Model):
    travel_allowance = models.DecimalField(max_digits=10,
                                        decimal_places=1,
                                        blank=True,
                                        null=True)
    daily_allowance = models.DecimalField(max_digits=10,
                                decimal_places=1,
                                blank=True,
                                null=True)
    user_id = models.ForeignKey(
        CompanyUserRole,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    date = models.DateField(
        blank=True,
        null=True
    )
    month = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    year = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    area_to = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    area_from = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    company_name = models.ForeignKey(Company, 
        on_delete=models.CASCADE, null=True, blank=True)
    # mpo_tour_plan = models.ForeignKey(
    #     CompanyMpoTourPlan,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True
    # )
    # higher_order_tour_plan = models.ForeignKey(
    #     HigherOrderTourplan,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True
    # )
