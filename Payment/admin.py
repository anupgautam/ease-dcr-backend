from django.contrib import admin
from Payment.models import *


payment_models = [Payment,
                    Bank,
                    CompanyWiseBank,
                    StockistPayment]
admin.site.register(payment_models)
