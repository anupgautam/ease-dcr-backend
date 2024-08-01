from django.db import models
from Company.models import Company
from django.contrib.auth.models import BaseUserManager

from DCRUser.models import CompanyUserRole
from django.apps import apps
from Mpo.models import CompanyMPOArea


class DoctorManger(BaseUserManager):
    def create_doctor_with_signal(self,
                                doctor_name,
                                doctor_address,
                                doctor_gender,
                                doctor_phone_number,
                                company_name,
                                doctor_territory,
                                doctor_category,
                                doctor_nmc_number,
                                doctor_specialization,
                                doctor_qualification,
                                mpo_name,
                                is_investment
                                ):
        doctor = Doctor(
            doctor_name=doctor_name,
            doctor_address=doctor_address,
            doctor_gender=doctor_gender,
            doctor_category=doctor_category,
            doctor_phone_number=doctor_phone_number,
            doctor_territory=doctor_territory,
            doctor_nmc_number=doctor_nmc_number,
            doctor_specialization=doctor_specialization,
            doctor_qualification=doctor_qualification
                )
        if company_name:
            doctor.company_name = company_name
        if mpo_name:
            doctor.mpo_name = mpo_name
        doctor.is_investment = is_investment
        doctor.save()
        return doctor

# This model stores the category of the doctor
class DoctorCategory(models.Model):
    category_name = models.CharField(max_length=400)
    def __str__(self):
        return self.category_name


class CompanyDoctorSpecialization(models.Model):
    company_name = models.ForeignKey(Company,
    on_delete=models.CASCADE)
    # category_name = models.ForeignKey(DoctorCategory,
    # on_delete=models.CASCADE)
    category_name = models.CharField(max_length=400,
                                     )


# This model stores the information about the doctor
class Doctor(models.Model):
    class Meta:
        ordering = ['-id']
    doctor_name = models.CharField(max_length=400,
                                   null=True,
                                   blank=True)
    doctor_address = models.CharField(max_length=400,
                                    null=True,
                                   blank=True)
    doctor_gender = models.CharField(max_length=400,
                                     blank=True,
                                     null=True)
    doctor_phone_number = models.CharField(max_length=20,
                                           blank=True,
                                           null=True)
    doctor_category = models.CharField(max_length=20,
                                   blank=True,
                                   null=True)
    doctor_nmc_number = models.CharField(max_length=200000,
                                          blank=True,
                                          null=True)
    doctor_qualification = models.CharField(max_length=200,
                                            blank=True,
                                            null=True)
    doctor_territory = models.ForeignKey(CompanyMPOArea,
                                         on_delete=models.CASCADE,
                                         )
    doctor_specialization = models.ForeignKey(CompanyDoctorSpecialization,
                                              on_delete=models.CASCADE)
    objects = DoctorManger()

    def __str__(self):
        return self.doctor_name

# This models stores the working area
# class DoctorWorkingArea(models.Model):
#     working_area_name = models.CharField(max_length=500)
#     def __str__(self):
#         return self.working_area_name

# This model stores the doctor according to the company
# class CategoryWiseDoctor(models.Model):
#     doctor_name = models.ForeignKey(Doctor,
#                                     on_delete=models.CASCADE)
#     doctor_category = models.ForeignKey(CompanyDoctorSpecialization,
#                                         on_delete=models.CASCADE)
#     class Meta:
#         ordering = ['-id']


# This model stores the doctors according to the company
class CompanyWiseDoctor(models.Model):
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)
    doctor_name = models.ForeignKey(Doctor,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)
    mpo_name = models.ForeignKey(
        CompanyUserRole,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    is_investment = models.BooleanField(null=True, blank=True)
                                    
    class Meta:
        ordering = ['-id']


class DoctorEvents(models.Model):
    doctor_id = models.ForeignKey(CompanyWiseDoctor,
                                  on_delete=models.CASCADE)
    event_title = models.CharField(max_length=1000)
    event_date = models.DateField()
    mpo_id = models.ForeignKey(CompanyUserRole, 
                               on_delete=models.CASCADE)
# class DoctorCompanyArea(models.Model):
#     company_name = models.ForeignKey(Company,
#     on_delete=models.CASCADE)
#     area_name = models.ForeignKey(DoctorWorkingArea,
#     on_delete=models.CASCADE)


# This model stores the doctor according ot the area
# class AreaWiseDoctor(models.Model):
#     doctor_name = models.ForeignKey(Doctor,
#                                     on_delete=models.CASCADE)
#     doctor_area = models.ForeignKey(DoctorCompanyArea,
#                                     on_delete=models.CASCADE)
