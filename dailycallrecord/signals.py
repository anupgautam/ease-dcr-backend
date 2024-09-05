from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from DCRUser.models import CompanyUserAttendance, CompanyUser, CompanyUserRole
from dailycallrecord.models import (
    MpoWiseShiftwiseDcrForChemist,
    MpoWiseShiftwiseDcrForStockist,
    MpoWiseShiftwiseDcrForDoctor,
    DcrForChemist,
    DcrForChemistProduct,
    StockistOrderedProduct,
    DcrForStockistOrderedProduct,
    ChemistOrderedProductInformationMap,
    MpoWiseShiftwiseDcrForChemist)
from Expenses.models import Target
from decimal import Decimal


@receiver(post_save, sender=MpoWiseShiftwiseDcrForDoctor)
def save_attendance_doctor(sender, instance, created, **kwargs):
    if created:
        if not CompanyUserAttendance.objects.filter(
            company_name=instance.mpo_name.company_name,
            user_id=instance.mpo_name,
            attendance_date=instance.dcr.dcr.date
        ).exists():
            company_user_attendance = CompanyUserAttendance(
                company_name=instance.mpo_name.company_name,
                user_id=instance.mpo_name,
                attendance_date=instance.dcr.dcr.date,
                is_present=True,
                month=instance.dcr.dcr.month,
            )
            company_user_attendance.save()


@receiver(post_save, sender=MpoWiseShiftwiseDcrForChemist)
def save_attendance_chemist(sender, instance, created, **kwargs):
    if created:
        if not CompanyUserAttendance.objects.filter(
            company_name=instance.mpo_name.company_name,
            user_id=instance.mpo_name,
            attendance_date=instance.dcr.dcr.date
        ).exists():
            company_user_attendance = CompanyUserAttendance(
                company_name=instance.mpo_name.company_name,
                user_id=instance.mpo_name,
                attendance_date=instance.dcr.dcr.date,
                month=instance.dcr.dcr.month,
                is_present=True
            )
            company_user_attendance.save()


@receiver(post_save, sender=MpoWiseShiftwiseDcrForStockist)
def save_attendance_stockist(sender, instance, created, **kwargs):
    if created:
        if not CompanyUserAttendance.objects.filter(
            company_name=instance.mpo_name.company_name,
            user_id=instance.mpo_name,
            attendance_date=instance.dcr.dcr.date,
            
        ).exists():
            company_user_attendance = CompanyUserAttendance(
                company_name=instance.mpo_name.company_name,
                user_id=instance.mpo_name,
                attendance_date=instance.dcr.dcr.date,
                month=instance.dcr.dcr.month,
                is_present=True
            )
            company_user_attendance.save()


@receiver(post_save, sender=MpoWiseShiftwiseDcrForChemist)
def create_or_update_target(sender, instance, created, **kwargs):
    if created:
        if not Target.objects.filter(target_to=instance.mpo_name).exists():
            Target.objects.create(
                year=instance.dcr.dcr.year,
                target_to=instance.mpo_name,
                target_from=CompanyUserRole.objects.get(user_name=instance.mpo_name.executive_level.user_name),
                target_amount=0.0,
                sales=0.0
            )


@receiver(post_save, sender=MpoWiseShiftwiseDcrForStockist)
def create_sales_data(sender, instance, created, **kwargs):
    target = Target.objects.get(target_to=instance.mpo_name)
    if created:
        dcr_for_stockist = instance.dcr.dcr
        dcr_stockist_ordered_product = DcrForStockistOrderedProduct.objects.filter(dcr_id=dcr_for_stockist)
        for dcr_stockist in dcr_stockist_ordered_product:
            stockist_price = dcr_stockist.ordered_product.ordered_product.product_name.product_price_for_stockist * dcr_stockist.ordered_product.ordered_quantity
            target.sales += Decimal(stockist_price)
        target.save()


@receiver(pre_delete, sender=MpoWiseShiftwiseDcrForStockist)
def delete_sales_data(sender, instance, **kwargs):
        target = Target.objects.get(target_to=instance.mpo_name)
        dcr_for_stockist = instance.dcr.dcr
        dcr_stockist_ordered_product = DcrForStockistOrderedProduct.objects.get(dcr_id=dcr_for_stockist)
        for dcr_stockist in dcr_stockist_ordered_product:
            stockist_price = dcr_stockist.ordered_product.ordered_product.product_name.product_price_for_stockist * dcr_stockist.ordered_product.ordered_quantity
            target.sales -= Decimal(stockist_price)
        target.save()


@receiver(post_save, sender=MpoWiseShiftwiseDcrForChemist)
def create_sales_data_chemist(sender, instance, created, **kwargs):
    target = Target.objects.get(target_to=instance.mpo_name)
    if created:
        dcr_for_chemist = instance.dcr.dcr
        dcr_for_chemist_product = DcrForChemistProduct.objects.get(dcr_id=dcr_for_chemist)
        dcr_chemist_map = ChemistOrderedProductInformationMap.objects.filter(product_id=dcr_for_chemist_product)
        for dcr_chemist in dcr_chemist_map:
            chemist_price = dcr_chemist.information_id.ordered_quantity * dcr_chemist.product_id.ordered_product.product_name.product_price_per_strip_in_mrp
            target.sales += Decimal(chemist_price)
        target.save()


@receiver(pre_delete, sender=MpoWiseShiftwiseDcrForChemist)
def delete_sales_data_chemist(sender, instance, **kwargs):
        target = Target.objects.get(target_to=instance.mpo_name)
        dcr_for_chemist = instance.dcr.dcr
        dcr_for_chemist_product = DcrForChemistProduct.objects.get(dcr_id=dcr_for_chemist)
        dcr_chemist_map = ChemistOrderedProductInformationMap.objects.filter(product_id=dcr_for_chemist_product)
        for dcr_chemist in dcr_chemist_map:
            chemist_price = dcr_chemist.information_id.ordered_quantity * dcr_chemist.product_id.ordered_product.product_name.product_price_per_strip_in_mrp
            target.sales -=  Decimal(chemist_price)
        target.save()


    
        

        