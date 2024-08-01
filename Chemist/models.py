from django.db import models
from Company.models import Company
from django.contrib.auth.models import BaseUserManager
from DCRUser.models import CompanyUserRole
from Mpo.models import CompanyMPOArea


class ChemistManager(BaseUserManager):
    def create_chemist_with_signal(self, 
                                    chemist_name,
                                    chemist_address,
                                    chemist_phone_number,
                                    company_name,
                                    chemist_territory,
                                    chemist_contact_person,
                                    chemist_pan_number,
                                    mpo_name,
                                    chemist_category,
                                    is_investment):
        chemist = Chemist(chemist_name=chemist_name,
                            chemist_address=chemist_address,
                            chemist_phone_number=chemist_phone_number,
                            chemist_territory=chemist_territory,
                            chemist_pan_number=chemist_pan_number,
                            chemist_contact_person=chemist_contact_person,
                            chemist_category=chemist_category
                            )
        if company_name:
            chemist.company_name = company_name
        if mpo_name:
            chemist.mpo_name = mpo_name
        chemist.is_investment = is_investment
        chemist.save()
        return chemist


# This model stores the category of the chemist
class ChemistCategory(models.Model):
    category_name = models.CharField(max_length=400)
    
    def __str__(self):
        return self.category_name


# This model stores the information about the chemist
class Chemist(models.Model):
    class Meta:
        ordering = ['-id']

    chemist_category = models.CharField(max_length=200)  
    chemist_name = models.CharField(max_length=400)
    chemist_address = models.CharField(max_length=400)
    chemist_phone_number = models.CharField(max_length=20, default=0)
    chemist_territory = models.ForeignKey(CompanyMPOArea,
                                          on_delete=models.CASCADE)
    chemist_contact_person = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    chemist_pan_number = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    objects = ChemistManager()

    def __str__(self):
        return self.chemist_name


# This models stores the working area
class ChemistWorkingArea(models.Model):
    working_area_name = models.CharField(max_length=500)


class ChemistCompanyArea(models.Model):
    company_name = models.ForeignKey(Company,
    on_delete=models.CASCADE)
    area_name = models.ForeignKey(ChemistWorkingArea,
    on_delete=models.CASCADE)


class CompanyChemistCategory(models.Model):
    company_name = models.ForeignKey(Company,
    on_delete=models.CASCADE)
    category_name = models.ForeignKey(ChemistCategory,
    on_delete=models.CASCADE)


# This model stores the chemists according to the chemist
class CompanyWiseChemist(models.Model):
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)
    chemist_name = models.ForeignKey(Chemist,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)
    mpo_name = models.ForeignKey(CompanyUserRole,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)
    is_investment = models.BooleanField(null=True, blank=True)
    class Meta:
        ordering = ['-id']
