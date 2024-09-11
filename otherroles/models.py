from django.db import models
from Mpo.models import CompanyMPOArea, CompanyUserRole
from Company.models import Company
from Mpo.models import Shift


class HigherOrderTourplan(models.Model):
    date = models.DateField()
    month = models.CharField(max_length=20,
                             default="January",
                             blank=True,
                             null=True)
    year = models.CharField(max_length=20,
                            default="2023",
                            blank=True,
                            null=True)
    visited_with = models.ForeignKey(CompanyUserRole,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)
    company_id = models.ForeignKey(Company,
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True)
    user_id = models.ForeignKey(CompanyUserRole,
                                on_delete=models.CASCADE,
                                related_name='user_id',
                                blank=True,
                                null=True)
    approved_by = models.ForeignKey(CompanyUserRole,
                                    on_delete=models.CASCADE,
                                    related_name='approved_by',
                                    blank=True,
                                    null=True)
    shift = models.ForeignKey(Shift,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True)
    is_approved = models.BooleanField(default=False)
    is_dcr_added = models.BooleanField(default=False)
    is_unplanned = models.BooleanField(default=False)
    is_admin_opened = models.BooleanField(default=False)
    hulting_station = models.CharField(max_length=50,
                                       null=True, blank=True,
                                       default="hulting")

    class Meta:
        ordering = ['-id']


class HigherOrderTourPlanVisit(models.Model):
    visited_with = models.ForeignKey(CompanyUserRole,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)
    # area = models.ForeignKey(
    #     CompanyMPOArea,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True)
    high_order_tour_plan_id = models.ForeignKey(
        HigherOrderTourplan,
        on_delete=models.CASCADE,
        blank=True,
        null=True) 


class HigherOrderDCR(models.Model):
    date = models.DateField()
    year = models.CharField(max_length=20,
                            default="2023")
    company_id = models.ForeignKey(Company,
                                   on_delete=models.CASCADE)
    user_id = models.ForeignKey(CompanyUserRole,
                                on_delete=models.CASCADE)
    visited_with = models.ForeignKey(CompanyUserRole,
                                     on_delete=models.CASCADE,
                                     related_name='visited_with')
    shift = models.ForeignKey(Shift,
                              on_delete=models.CASCADE) 
    month = models.CharField(default="January",max_length=20)

    class Meta:
        ordering = ['-id']
