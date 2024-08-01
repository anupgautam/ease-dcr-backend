from django.contrib import admin
from DCRUser.models import *


user_models = [
                CompanyUser,
                CompanyUserRole
                ]
admin.site.register(user_models)
