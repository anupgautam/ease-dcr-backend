from re import T
from django.db import models
from Company.models import Company
from Stockist.models import Stockist


# This model stores the names of the banks
class Bank(models.Model):
    bank_name = models.CharField(max_length=1000)


# This model stores the names of banks according to the company
class CompanyWiseBank(models.Model):
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE)
    bank_name = models.ForeignKey(Bank,
                                  on_delete=models.CASCADE)


# This model stores all the details of the payment and transaction
class Payment(models.Model):
    payment_received_date = models.DateField()
    payment_bank_name = models.ForeignKey(Bank,
                                          on_delete=models.CASCADE)
    payment_cheque_amount = models.FloatField()
    payment_clearing_date = models.DateField()


# This model stores the payment of the Stockist
class StockistPayment(models.Model):
    stockist_name = models.ForeignKey(Stockist,
                                      on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,
                                on_delete=models.CASCADE)
