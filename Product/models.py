from django.db import models
from django.contrib.auth.models import (
    BaseUserManager
)

from Company.models import (Company, CompanyWiseDivision)
from DCRUser.models import User


class ProductManager(BaseUserManager):
    def create_product_with_signal(
                                    self,   
                                    product_name,
                                    product_molecular_name,
                                    product_price_per_strip_in_mrp,
                                    product_price_for_stockiest,
                                    company_name,
                                    division_name,
                                    mpo_name
    ):
        product = Product(product_name=product_name,
                             product_molecular_name=product_molecular_name,
                             product_price_per_strip_in_mrp=product_price_per_strip_in_mrp,
                             product_price_for_stockiest=product_price_for_stockiest)
        product.company_name = company_name
        product.division_name = division_name
        product.save() 
        return product


# This model is for the storing the timestamp of creation and updation
class TimeStamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

# This model stores the general information about the product
class Product(TimeStamp, models.Model):
    product_name = models.CharField(max_length=600)
    product_molecular_name = models.CharField(max_length=1000)
    product_price_per_strip_in_mrp = models.FloatField()
    product_price_for_stockist = models.FloatField()
    product_description = models.TextField(blank=True, null=True)
    product_image = models.ImageField(upload_to='media', blank=True, null=True)
    objects = ProductManager()
    class Meta:
        ordering = ['-id']


# This model stores the product according to the company
PRODUCT_TYPE_CHOICES = (
    ('liquid', 'Liquid'),
    ('tab', 'Tablet'),
    ('cap', 'Capsules'),
    ('tm', 'Topical Medicines'),
    ('sup', 'Suppositories'),
    ('drop', 'Drops'),
    ('inhaler', 'Inhalers'),
    ('injection', 'Injections'),
    ('implant', 'Implants'),
    ('buccal', 'Buccal')
)
class CompanyProduct(TimeStamp, models.Model):
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product,
                                     on_delete=models.CASCADE)
    batch_no = models.CharField(null=True, blank=True, max_length=100)
    product_type = models.CharField(
        null=True, blank=True, max_length=10, choices=PRODUCT_TYPE_CHOICES)
    bonus = models.CharField(null=True, blank=True, max_length=10)
    
    class Meta:
        ordering = ['-id']


class CompanyDivisionProduct(TimeStamp, models.Model):
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE)
    division_name = models.ForeignKey(CompanyWiseDivision,
                                      on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product,
                                     on_delete=models.CASCADE)
    product_type = models.CharField(
        null=True, blank=True, max_length=10, choices=PRODUCT_TYPE_CHOICES)
    bonus = models.CharField(null=True, blank=True, max_length=10)
    class Meta:
        ordering = ['-id']


# class CompanyMpoWiseProduct(TimeStamp, models.Model):
#     company_name = models.ForeignKey(Company,
#                                      on_delete=models.CASCADE)
#     product_name = models.ForeignKey(Product,
#                                      on_delete=models.CASCADE)
#     mpo_name = models.ForeignKey(CompanyMpo,
#                                 on_delete=models.CASCADE)
    
#     class Meta:
#         ordering = ['-id']
