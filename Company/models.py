from django.db import models
from django.contrib.auth.models import BaseUserManager
from rest_framework.response import Response


class NoticeManager(BaseUserManager):
    def create_notice_using_signal(self, notice_name, notice_description, company_name):
        notice = Notices(
            notice_name=notice_name,
            notice_description=notice_description,
        )
        notice.company_name = company_name
        notice.save()
        return notice


# This models stores the general infromation about the companies
class Company(models.Model):
    class Meta:
        ordering = ["-company_id"]

    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=300)
    company_address = models.CharField(max_length=300)
    company_phone_number = models.CharField(max_length=20, null=True, blank=True)
    company_email_address = models.EmailField()

    def __str__(self):
        return self.company_name


# This model stores all the division names
class Division(models.Model):
    # division_id = models.AutoField(primary_key=True)
    division_name = models.CharField(max_length=300)

    def __str__(self):
        return self.division_name


# This model store all the roles
class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=300)

    def __str__(self):
        return self.role_name


# This model stores all the notices and its description
class Notices(models.Model):
    # notice_id = models.AutoField(primary_key=True)
    notice_name = models.CharField(max_length=400)
    notice_description = models.TextField()
    objects = NoticeManager()


# This model stores the names of working hour
class WorkingHour(models.Model):
    working_hour = models.CharField(max_length=10)

    def __str__(self):
        return self.working_hour


# This model stores the division name accoring to the company
class CompanyWiseDivision(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
    division_name = models.CharField(max_length=200)


# This model stores the notices according to the company
class CompanyNotices(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
    notice_name = models.ForeignKey(Notices, on_delete=models.CASCADE)


# This model stores the working area according to the companies
class CompanyArea(models.Model):
    company_name = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=True, null=True
    )
    company_area = models.CharField(null=True, blank=True, max_length=20)
    station_type = models.CharField(null=True, blank=True, max_length=20)


class CompanyHoliday(models.Model):
    company_name = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=True, null=True
    )
    holiday_name = models.CharField(max_length=100, blank=True, null=True)


class CompanyHolidayArea(models.Model):
    company_area = models.ForeignKey(
        CompanyArea, on_delete=models.CASCADE, null=True, blank=True
    )
    holiday_type = models.ForeignKey(
        CompanyHoliday, on_delete=models.CASCADE, null=True, blank=True
    )


# This model stores the working hour according to the companies
class CompanyWorkingHour(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_working_hour = models.ForeignKey(WorkingHour, on_delete=models.CASCADE)


# This model stores the roles accoring to company
class CompanyRoles(models.Model):
    company_name = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )
    role_name = models.ForeignKey(
        Roles, on_delete=models.CASCADE, blank=True, null=True
    )
    priority_value = models.IntegerField(null=True, blank=True)
    role_name_value = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.role_name.role_name


# This model stores the salary according to the roles of the company
class CompanySalaryRoles(models.Model):
    company_roles = models.ForeignKey(CompanyRoles, on_delete=models.CASCADE)
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
    salary = models.IntegerField()


class CompanyHolidayDate(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
    holiday_date = models.DateField()
    company_holiday_area = models.ForeignKey(
        CompanyHolidayArea, on_delete=models.CASCADE, null=True, blank=True
    )
