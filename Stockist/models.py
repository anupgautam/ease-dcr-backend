from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from Company.models import Company, CompanyArea
from DCRUser.models import CompanyUserRole
from Mpo.models import CompanyMPOArea


class StockistManager(BaseUserManager):
    def create_stockist_with_signal(self, stockist_name,
                                     stockist_address,
                                     stockist_contact_number,
                                     stockist_territory,
                                     pan_vat_number,
                                     company_name,
                                     stockist_category,
                                     ):
        company_area = CompanyArea.objects.get(id=stockist_territory)
        stockist = Stockist(stockist_name=stockist_name,
                             stockist_address=stockist_address,
                             stockist_contact_number=stockist_contact_number,
                             stockist_territory=company_area,
                             pan_vat_number=pan_vat_number,
                             stockist_category=stockist_category
                            )
        if company_name:
            stockist.company_name = company_name
        stockist.save() 
        return stockist 


class Stockist(models.Model):
    class Meta:
        ordering = ['-id']

    stockist_category = models.CharField(max_length=400)
    stockist_name = models.CharField(max_length=500)
    stockist_contact_number = models.CharField(max_length=20)
    stockist_address = models.CharField(max_length=500)
    stockist_territory = models.ForeignKey(CompanyArea,
                                          on_delete=models.CASCADE)
    pan_vat_number = models.CharField(max_length=50, null=True, blank=True)
    objects = StockistManager()
    

# This model stores the stockist according to the company
class CompanyStockist(models.Model):
    class Meta:
        ordering = ['-id']
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE, 
                                     blank=True,
                                     null=True)
    stockist_name = models.ForeignKey(Stockist,
                                      on_delete=models.CASCADE,
                                      blank=True,
                                      null=True)
    

class CompanyMPOStockist(models.Model):
    stockist_name = models.ForeignKey(
        CompanyStockist,
        on_delete=models.CASCADE,
        blank=True, null=True)
    mpo_name = models.ForeignKey(
        CompanyUserRole,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    company_name = models.ForeignKey(
        Company,
        on_delete=models.CASCADE, 
        blank=True,
        null=True)
             