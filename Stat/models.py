from django.db import models
from Chemist.models import CompanyWiseChemist

from Company.models import Company
from DCRUser.models import CompanyUserRole
from Doctors.models import CompanyWiseDoctor, Doctor
from Mpo.models import CompanyMPOArea

# Create your models here.

class CompanyDCRTourPlanValidity(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    days = models.IntegerField(null=False, blank=False, default=1)


class MPOMissedCallModel(models.Model):
    mpo_name = models.ForeignKey(CompanyUserRole,
                                on_delete=models.CASCADE,
                                related_name="%(class)s_mpo_name",
                                blank=True,
                                null=True)
    company_name = models.ForeignKey(Company,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)
    doctor = models.ForeignKey(CompanyWiseDoctor, on_delete=models.CASCADE, blank=True, null=True)
    chemist = models.ForeignKey(CompanyWiseChemist, on_delete=models.CASCADE, blank=True, null=True)
    remarks = models.TextField(null=True, blank=True)
    month = models.CharField(null=True, blank=True, max_length=10)
    year = models.CharField(null=True, blank=True, max_length=10)
