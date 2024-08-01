from django.contrib import admin
from Stockist.models import *


stockist_model = [Stockist,
                  CompanyStockist]
admin.site.register(stockist_model)
