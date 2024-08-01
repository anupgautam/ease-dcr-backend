from django.contrib import admin
from Product.models import *


product_models = [Product,
                  CompanyProduct,
                  CompanyDivisionProduct,
                  ]
admin.site.register(product_models)
