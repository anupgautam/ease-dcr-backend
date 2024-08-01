from django.contrib import admin
from Expenses.models import *


expenses_models = [ExpensesType,
                    ]
admin.site.register(expenses_models)
