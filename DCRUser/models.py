from django.db import models
from rest_framework.response import Response
from django.contrib.auth.models import BaseUserManager
# from phonenumber_field.modelfields import PhoneNumberField
from Company.models import (Company, Roles)
from Account.models import User
from Company.models import CompanyRoles, CompanyWiseDivision, CompanyArea



# # This model stores the general information about the user
# class User(models.Model):
#     user_name = models.CharField(max_length=500, blank=True)
#     user_address = models.CharField(max_length=500, blank=True)
#     # gender
#     # user_phone_number = PhoneNumberField()
class CompanyManger(BaseUserManager):
    def create_company_user_role(self,first_name,
                            last_name,
                            email,
                            contact_number,
                            address,
                            role_name
                            ):
        user = User.objects.create(first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=contact_number,
        )
        user.address = address
        user.role_name = role_name
        user.save()
        return user


# This model stores the user according to the company
class CompanyUser(models.Model):
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE)
    user_name = models.ForeignKey(User,
                                  on_delete=models.CASCADE)


# This model stores the user according to the role and company
class CompanyUserRole(models.Model):
    class Meta:
        ordering=['-id']
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)
    user_name = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True)
    role_name = models.ForeignKey(CompanyRoles,
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True)
    division_name = models.ForeignKey(CompanyWiseDivision,
                                      on_delete=models.CASCADE,
                                      blank=True,
                                      null=True)
    executive_level = models.ForeignKey(CompanyUser,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True)
    company_area = models.ForeignKey(CompanyArea, 
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)
    station_type = models.CharField(max_length=200,
                                    blank=True,
                                    null=True)
    is_tp_locked = models.BooleanField(null=False, blank=False, default=False)
    objects = CompanyManger()



class CompanyUserAttendance(models.Model):
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE)
    user_id = models.ForeignKey(CompanyUserRole, on_delete=models.CASCADE)
    attendance_date = models.DateField(blank=True,null=True)
    month = models.CharField(null=True, blank=True, max_length=50, default="Baisakh")
    is_leave = models.BooleanField(null=False, blank=False, default=False)
    leave_type = models.CharField(null=True, blank=True, max_length=100)
    is_saturday = models.BooleanField(null=False,blank=False, default=False)
    is_present = models.BooleanField(null=False,blank=False,default=False)
    is_holiday = models.BooleanField(null=False,blank=False,default=False)
    

