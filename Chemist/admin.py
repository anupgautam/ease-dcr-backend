from django.contrib import admin
from Chemist.models import *


chemist_models = [Chemist,
                  ChemistCategory,
                  ChemistWorkingArea,
                #   CategoryWiseChemist,
                  CompanyWiseChemist,
                  # AreaWisechemist,
                  ]
admin.site.register(chemist_models)
