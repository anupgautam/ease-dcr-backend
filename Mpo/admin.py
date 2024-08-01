from django.contrib import admin
from Mpo.models import *


mpo_models = [
              CompanyDivisionWiseMpo,
              PurposeOfVisit,
              TourPlan,
              CompanyMpoTourPlan,
              ActiveWorkingDays,
              Shift
              ]
admin.site.register(mpo_models)