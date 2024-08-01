from django.contrib import admin
from .models import *


dcr_models = [
    Rewards,
    DcrForDoctor,
    DcrForChemist,
    DcrForStockist,
    ShiftWiseDcrForDoctor,
    ShiftWiseDcrForChemist,
    ShiftWiseDcrForStockist
]

admin.site.register(dcr_models)
