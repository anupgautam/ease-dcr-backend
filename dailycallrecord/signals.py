from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from DCRUser.models import CompanyUserAttendance, CompanyUser, CompanyUserRole
from dailycallrecord.models import (
    MpoWiseShiftwiseDcrForChemist,
    MpoWiseShiftwiseDcrForStockist,
    MpoWiseShiftwiseDcrForDoctor,
    DcrForChemist,
    StockistOrderedProduct,
    DcrForStockistOrderedProduct,
    ChemistOrderedProductInformationMap,
    MpoWiseShiftwiseDcrForChemist)
from Expenses.models import Target


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
                month=instance.dcr.dcr.month
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
                month=instance.dcr.dcr.month
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
                month=instance.dcr.dcr.month
            )
            company_user_attendance.save()


@receiver(post_save, sender=MpoWiseShiftwiseDcrForChemist)
def create_or_update_target(sender, instance, created, **kwargs):
    if created:
        if not Target.objects.filter(target_to=instance.visited_area.mpo_name).exists():
            Target.objects.create(
                year=instance.year,
                target_to=instance.visited_area.mpo_name,
                target_from=CompanyUserRole.objects.get(user_name=instance.visited_area.mpo_name.executive_level),
                target_amount=0.0,
                sales=0.0
            )


@receiver(post_save, sender=DcrForStockistOrderedProduct)
def create_sales_data(sender, instance, created, **kwargs):
    mpo_name = MpoWiseShiftwiseDcrForStockist.objects.get(dcr__dcr=instance.produdct_id.dcr_id)
    target = Target.objects.get(target_to=mpo_name)
    if created:
        stockist_price = instance.ordered_product.ordered_product.product_name.product_price_for_stockist * instance.ordered_product.ordered_quantity
        target.sales += stockist_price
        target.save()


@receiver(pre_delete, sender=DcrForStockistOrderedProduct)
def delete_sales_data(sender, instance, **kwargs):
        mpo_name = MpoWiseShiftwiseDcrForStockist.objects.get(dcr__dcr=instance.produdct_id.dcr_id)
        target = Target.objects.get(target_to=mpo_name)
        stockist_price = instance.ordered_product.ordered_product.product_name.product_price_for_stockist * instance.ordered_product.ordered_quantity
        target.sales -= stockist_price
        target.save()


@receiver(post_save, sender=ChemistOrderedProductInformationMap)
def create_sales_data_chemist(sender, instance, created, **kwargs):
    mpo_name = MpoWiseShiftwiseDcrForChemist.objects.get(dcr__dcr=instance.produdct_id.dcr_id)
    target = Target.objects.get(target_to=mpo_name)
    if created:
        chemist_price = instance.information_id.ordered_quantity * instance.product_id.ordered_product.product.product_price_per_strip_in_mrp
        target.sales += chemist_price
        target.save()


@receiver(pre_delete, sender=ChemistOrderedProductInformationMap)
def delete_sales_data_chemist(sender, instance, **kwargs):
        mpo_name = MpoWiseShiftwiseDcrForChemist.objects.get(dcr__dcr=instance.produdct_id.dcr_id)
        target = Target.objects.get(target_to=mpo_name)
        chemist_price = instance.information_id.ordered_quantity * instance.product_id.ordered_product.product.product_price_per_strip_in_mrp
        target.sales -= chemist_price
        target.save()


    
        

        