from django.db import models

from Stockist.models import CompanyStockist
from Product.models import CompanyProduct
from Company.models import Company

# Create your models here.
class SecondarySales(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE,
                                     null=True, blank=True)
    stockist = models.ForeignKey(
        CompanyStockist, on_delete=models.CASCADE,
        null=True, blank=True)
    year = models.CharField(null=True, blank=True, max_length=10)
    month = models.CharField(null=True, blank=True, max_length=10)
    product = models.ForeignKey(
        CompanyProduct, on_delete=models.CASCADE,
        null=True, blank=True)
    opening_stock = models.IntegerField(null=True, blank=True)
    purchase = models.IntegerField(null=True, blank=True)
    sales_return = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    sales = models.IntegerField(null=True, blank=True)
    free = models.IntegerField(null=True, blank=True)
    exchange_breakage = models.IntegerField(null=True, blank=True)
    closing_stock = models.IntegerField(null=True, blank=True)
    l_rate = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=10)
    st_value = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=10)
    sl_value = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=10)
    

class PrimarySales(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE,
                                     null=True, blank=True)
    stockist = models.ForeignKey(
        CompanyStockist, on_delete=models.CASCADE,
        null=True, blank=True)
    year = models.CharField(null=True, blank=True, max_length=10)
    month = models.CharField(null=True, blank=True, max_length=10)
    product = models.ForeignKey(
        CompanyProduct, on_delete=models.CASCADE,
        null=True, blank=True)
    opening_stock = models.IntegerField(null=True, blank=True)
    purchase = models.IntegerField(null=True, blank=True)
    sales_return = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    sales = models.IntegerField(null=True, blank=True)
    free = models.IntegerField(null=True, blank=True)
    exchange_breakage = models.IntegerField(null=True, blank=True)
    closing_stock = models.IntegerField(null=True, blank=True)
    l_rate = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=10)
    st_value = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=10)
    sl_value = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=10)