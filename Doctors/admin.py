from django.contrib import admin
from Doctors.models import *


doctor_models = [Doctor,
                 DoctorCategory,
                #  DoctorWorkingArea,
                #  CategoryWiseDoctor,
                CompanyDoctorSpecialization,
                 CompanyWiseDoctor,
                #  AreaWiseDoctor,
                 ]
admin.site.register(doctor_models)
