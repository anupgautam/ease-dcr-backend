from django.db import models
from Doctors.models import Doctor, CompanyWiseDoctor
from Product.models import CompanyProduct
from Company.models import CompanyRoles, Company
from Stockist.models import CompanyStockist
from Mpo.models import Shift
from Product.models import Product
from Stockist.models import CompanyStockist
from DCRUser.models import CompanyUserRole
from Chemist.models import CompanyWiseChemist
from Mpo.models import ActiveWorkingDays, CompanyMPOArea
from Company.models import CompanyArea
from django.core.validators import DecimalValidator


# This model is used to store the timestamp
class TimeStamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# This model stores the rewards
class Rewards(TimeStamp, models.Model):
    reward = models.CharField(max_length=200,
    blank=True,
    null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                blank=True,
                                null=True)
    company_name = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True, blank=True)



# This model stores the dcr of doctor
class DcrForDoctor(TimeStamp, models.Model):
    date = models.DateField(blank=True,
                            null=True)
    visited_area = models.ForeignKey(CompanyMPOArea,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)
    visited_doctor = models.ForeignKey(CompanyWiseDoctor,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    month = models.CharField(max_length=20,
                             blank=True,
                             null=True)
    year = models.CharField(max_length=10,
                            blank=True,
                            null=True)
    expenses_name = models.CharField(max_length=400,
                                     blank=True,
                                     null=True)
    # expenses = models.DecimalField(max_digits=20,
    # decimal_places=2, null=True, blank=True)
    expenses = models.IntegerField(blank=True,null=True)
    expenses_reasoning = models.TextField(blank=True,
                                          null=True)


class DcrForDoctorCompanyProductMap(models.Model):
    dcr_id = models.ForeignKey(DcrForDoctor,
                               on_delete=models.CASCADE)
    company_product_id = models.ForeignKey(CompanyProduct,
                                           on_delete=models.CASCADE)


class DcrForDoctorRewardsMap(models.Model):
    dcr_id = models.ForeignKey(DcrForDoctor,
                               on_delete=models.CASCADE)
    reward_id = models.ForeignKey(Rewards,
                                        on_delete=models.CASCADE)
    

class DcrForDoctorCompanyRolesMap(models.Model):
    dcr_id = models.ForeignKey(DcrForDoctor,
                               on_delete=models.CASCADE)
    roles_id = models.ForeignKey(CompanyUserRole,
                                        on_delete=models.CASCADE)


# This model stores the dcr of the specific doctor according to the shift
class ShiftWiseDcrForDoctor(TimeStamp, models.Model):
    shift = models.ForeignKey(
        Shift, on_delete=models.CASCADE
    )
    dcr = models.ForeignKey(
        DcrForDoctor, on_delete=models.CASCADE
    )


# This model stores the dcr of the doctor along with the shift
# of the specific mpo
class MpoWiseShiftwiseDcrForDoctor(TimeStamp, models.Model):
    mpo_name = models.ForeignKey(
    CompanyUserRole, on_delete=models.CASCADE)
    dcr = models.ForeignKey(
        ShiftWiseDcrForDoctor, on_delete=models.CASCADE
    )


class ChemistOrderedProduct(TimeStamp, models.Model):
    ordered_product = models.ForeignKey(
        CompanyProduct, on_delete=models.CASCADE,
        null=True, blank=True
    )


class ChemistOrderedProductInformation(TimeStamp, models.Model):
    ordered_quantity = models.IntegerField(
                                        null=True,
                                        blank=True)
    select_the_stockist = models.ForeignKey(
        CompanyStockist, on_delete=models.CASCADE,
        null=True,
        blank=True
    )


class ChemistOrderedProductInformationMap(TimeStamp, models.Model):
    product_id = models.ForeignKey(CompanyProduct,
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True)
    information_id = models.ForeignKey(
        ChemistOrderedProductInformation,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


# This model stores the dcr of chemist
class DcrForChemist(TimeStamp, models.Model):
    date = models.DateField(blank=True, null=True)
    visited_area = models.ForeignKey(CompanyMPOArea,
                                     on_delete=models.CASCADE,
                                     blank=True,
                             null=True)
    visited_chemist = models.ForeignKey(
        CompanyWiseChemist,on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    month = models.CharField(max_length=20, default="January")
    year = models.CharField(max_length=10, default=2023)
    expenses_name = models.CharField(max_length=400, blank=True, null=True)
    # expenses = models.DecimalField(max_digits=10,
    # decimal_places=9, null=True, blank=True)
    expenses = models.IntegerField(blank=True,null=True)
    expenses_reasoning = models.TextField(blank=True,null=True)
    

class DcrForChemistProduct(TimeStamp, models.Model):
    dcr_id = models.ForeignKey(DcrForChemist,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)
    ordered_product = models.ForeignKey(
        CompanyProduct, on_delete=models.CASCADE,
        blank=True,
        null=True
    )


#This map is for the promoted product
class DcrForChemistPromotedProductMap(models.Model):
    dcr_id = models.ForeignKey(DcrForChemist,
                               on_delete=models.CASCADE)
    company_product_id = models.ForeignKey(CompanyProduct,
                                           on_delete=models.CASCADE)


class DcrForChemistRewardsMap(models.Model):
    dcr_id = models.ForeignKey(DcrForChemist,
                               on_delete=models.CASCADE)
    reward_id = models.ForeignKey(Rewards,
                                        on_delete=models.CASCADE)
    

class DcrForChemistCompanyRolesMap(models.Model):
    dcr_id = models.ForeignKey(DcrForChemist,
                               on_delete=models.CASCADE)
    roles_id = models.ForeignKey(CompanyUserRole,
                                        on_delete=models.CASCADE)
    
    
# This model stores the dcr of the specific chemist according to the shift
class ShiftWiseDcrForChemist(TimeStamp, models.Model):
    shift = models.ForeignKey(
        Shift, on_delete=models.CASCADE
    )
    dcr = models.ForeignKey(
        DcrForChemist, on_delete=models.CASCADE
    )


# This model stores the dcr of the Chemist along with the shift
# of the specific mpo
class MpoWiseShiftwiseDcrForChemist(TimeStamp, models.Model):
    mpo_name = models.ForeignKey(
    CompanyUserRole, on_delete=models.CASCADE)
    dcr = models.ForeignKey(
        ShiftWiseDcrForChemist, on_delete=models.CASCADE
    )

class StockistOrderedProduct(TimeStamp, models.Model):
    ordered_product = models.ForeignKey(
        CompanyProduct, on_delete=models.CASCADE,
        null=True, blank=True
    )
    ordered_quantity = models.IntegerField(
                                        null=True,
                                        blank=True)
    order_value = models.DecimalField(max_digits=10,
    decimal_places=3, null=True, blank=True)


# This model stores the dcr of stockist
class DcrForStockist(TimeStamp, models.Model):
    date = models.DateField(blank=True, null=True)
    visited_area = models.ForeignKey(CompanyMPOArea,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)
    visited_stockist = models.ForeignKey(
        CompanyStockist,on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    month = models.CharField(max_length=20,
                             blank=True,
                             null=True)
    year = models.CharField(max_length=10,
                            blank=True,
                            null=True)
    expenses_name = models.CharField(max_length=400,
                                     blank=True,
                                     null=True)
    # expenses = models.DecimalField(max_digits=10,
    #                                decimal_places=9,
    #                                null=True,
    #                                blank=True)
    expenses = models.IntegerField(blank=True,null=True)
    expenses_reasoning = models.TextField(blank=True,
                                          null=True)


class DcrForStockistOrderedProduct(TimeStamp, models.Model):
    dcr_id = models.ForeignKey(DcrForStockist,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)
    ordered_product = models.ForeignKey(
        StockistOrderedProduct, on_delete=models.CASCADE,
        blank=True,
        null=True
    )


#This map is for the promoted product
class DcrForStockistOrderedProductMap(models.Model):
    dcr_id = models.ForeignKey(DcrForStockist,
                               on_delete=models.CASCADE)
    company_product_id = models.ForeignKey(CompanyProduct,
                                           on_delete=models.CASCADE)


class DcrForStockistRewardsMap(models.Model):
    dcr_id = models.ForeignKey(DcrForStockist,
                               on_delete=models.CASCADE)
    reward_id = models.ForeignKey(Rewards,
                                        on_delete=models.CASCADE)
    

class DcrForStockistCompanyRolesMap(models.Model):
    dcr_id = models.ForeignKey(DcrForStockist,
                               on_delete=models.CASCADE)
    roles_id = models.ForeignKey(CompanyUserRole,
                                        on_delete=models.CASCADE)
   

# This model stores the dcr of the specific stockist according to the shift
class ShiftWiseDcrForStockist(TimeStamp, models.Model):
    shift = models.ForeignKey(
        Shift, on_delete=models.CASCADE
    )
    dcr = models.ForeignKey(
        DcrForStockist, on_delete=models.CASCADE
    )


# This model stores the dcr of the Stockist along with the shift
# of the specific mpo
class MpoWiseShiftwiseDcrForStockist(TimeStamp, models.Model):
    mpo_name = models.ForeignKey(
    CompanyUserRole, on_delete=models.CASCADE)
    dcr = models.ForeignKey(
        ShiftWiseDcrForStockist, on_delete=models.CASCADE
    )
