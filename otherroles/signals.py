from django.db.models.signals import post_save
from django.dispatch import receiver
from DCRUser.models import CompanyUserAttendance
from otherroles.models import HigherOrderDCR


@receiver(post_save, sender=HigherOrderDCR)
def save_attendance_high_order(sender, instance, created, **kwargs):
    if created:
        if not CompanyUserAttendance.objects.filter(
            company_name=instance.company_id,
            user_id=instance.user_id,
            attendance_date=instance.date
        ).exists():
            company_user_attendance = CompanyUserAttendance(
                company_name=instance.company_id,
                user_id=instance.user_id,
                attendance_date=instance.date,
                month=instance.month
            )
            company_user_attendance.save()