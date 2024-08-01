from collections.abc import Iterable
from django.db import models

from Company.models import (Company,
                            Division,
                            CompanyArea)
from DCRUser.models import CompanyUserRole
from nepali_datetime_field.models import NepaliDateField
from DCR import settings
# from Doctors.models import Doctor


class Shift(models.Model):
    shift = models.CharField(max_length=200,
                             blank=True,
                             null=True)


# This model stores the mpo according to the company and division
class CompanyDivisionWiseMpo(models.Model):
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE)
    mpo_name = models.ForeignKey(CompanyUserRole,
                                 on_delete=models.CASCADE)
    division_name = models.ForeignKey(Division,
                                      on_delete=models.CASCADE)


# This model stores the purpose of visit
class PurposeOfVisit(models.Model):
    purpose_of_visit = models.CharField(max_length=250)


class ActiveWorkingDays(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                 related_name='%(class)s_company',
                                 blank=True,
                                 null=True)
    date = models.DateField(null=True, blank=True)
    is_holiday = models.BooleanField(null=True, blank=True)

class CompanyMPOArea(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    mpo_name = models.ForeignKey(
        CompanyUserRole,
        on_delete=models.CASCADE,
        related_name='%(class)s_mpo',
        blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        blank=True,
        null=True
        )
    country = models.CharField(blank=True, null=True, max_length=400)
    state = models.CharField(blank=True, null=True, max_length=400)
    division = models.CharField(blank=True, null=True, max_length=400)
    area_name = models.CharField(max_length=400)
    station_type = models.CharField(
        max_length=20)
    company_area = models.ForeignKey(
        CompanyArea,
        on_delete=models.CASCADE,
        related_name='%(class)s_mpo',
        blank=True, null=True
    )


# This model stores the tourplan
class TourPlan(models.Model):
    year = models.CharField(max_length=10, blank=True, null=True)
    select_the_month = models.CharField(max_length=100,
                                        blank=True,
                                        null=True)
    select_the_date_id = models.DateField(blank=True, null=True)
    # select_the_date_id = NepaliDateField()
    purpose_of_visit = models.CharField(max_length=300, blank=True, null=True)
    is_dcr_added = models.BooleanField(default=False, blank=True, null=True)
    is_doctor_dcr_added = models.BooleanField(default=False, blank=True, null=True)
    is_chemist_dcr_added = models.BooleanField(default=False, blank=True, null=True)
    is_stockist_dcr_added = models.BooleanField(default=False, blank=True, null=True)
    is_unplanned = models.BooleanField(default=False, blank=True, null=True)
    is_admin_opened = models.BooleanField(default=False, blank=True, null=True)
    hulting_station = models.CharField(max_length=50,
                                       null=True, blank=True,
                                       default="hulting")

    def save(self, *args, **kwargs):
        if self.select_the_date_id:
            self.year = self.select_the_date_id.year
        super(TourPlan, self).save(*args, **kwargs)


class CompanyMPOAreaTourPlan(models.Model):
    tour_plan_id = models.ForeignKey(
        TourPlan, on_delete=models.CASCADE, null=True, blank=True)
    company_mpo_area_id = models.ForeignKey(
        CompanyMPOArea,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='company_mpo_area_id'
    )

    
#This model stores the tourplan according to the shift
class ShiftWiseTourplan(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, blank=True, null=True)
    tour_plan = models.ForeignKey(TourPlan, on_delete=models.CASCADE)


# This model stores the tourplan of the mpo accoring to mpo and company
class CompanyMpoTourPlan(models.Model):
    mpo_name = models.ForeignKey(CompanyUserRole,
                                on_delete=models.CASCADE,
                                related_name="mpo_mpo_name",
                                blank=True,
                                null=True)
    company_name = models.ForeignKey(Company,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)
    tour_plan = models.ForeignKey(ShiftWiseTourplan,
                                on_delete=models.CASCADE)
    approved_by = models.ForeignKey(CompanyUserRole,
                                on_delete=models.CASCADE,
                                related_name='mpo_approved_by',
                                blank=True,
                                null=True
                                )
    is_approved = models.BooleanField(default=False,blank=True, null=True)
    is_missed_call_calculated = models.BooleanField(default=False, blank=True, null=True)
    class Meta:
        ordering = ['-id']


# class CompanyMPODoctor(models.Model):
#     company_name = models.ForeignKey(Company,
#                                      on_delete=models.CASCADE,
#                                      blank=True,
#                                      null=True)
#     doctor_name = models.ForeignKey(Doctor,
#                                     on_delete=models.CASCADE,
#                                     blank=True,
#                                     null=True)
#     company_area = models.ForeignKey(CompanyMPOArea,
#                                      on_delete=models.CASCADE,
#                                      blank=True, null=True)
#     mpo_name = models.ForeignKey(CompanyUserRole,
#                                  on_delete=models.CASCADE,
#                                  blank=True, null=True)

