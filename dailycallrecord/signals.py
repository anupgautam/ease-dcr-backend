from django.db.models.signals import post_save
from django.dispatch import receiver
from DCRUser.models import CompanyUserAttendance
from dailycallrecord.models import (
    MpoWiseShiftwiseDcrForChemist,
    MpoWiseShiftwiseDcrForStockist,
    MpoWiseShiftwiseDcrForDoctor)


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
        