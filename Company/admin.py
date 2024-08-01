from django.contrib import admin
from Company.models import *


company_models = [Company,
                  CompanyArea,
                  Roles,
                  CompanyRoles,
                  Notices,
                  CompanyNotices,
                  Division,
                  CompanyWiseDivision,
                  WorkingHour,
                  CompanyWorkingHour]
admin.site.register(company_models)
