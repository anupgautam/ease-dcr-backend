from datetime import timedelta
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from DCRUser.models import CompanyUserAttendance
from Expenses.models import MpoWiseLeaveApplication
from DCRUser.utils import month_number_to_name


@receiver(post_save, sender=MpoWiseLeaveApplication)
def save_leave_application(sender, instance, created, **kwargs):
    if not created:
        if not CompanyUserAttendance.objects.filter(
            company_name=instance.mpo_name.company_name,
            user_id=instance.mpo_name,
            attendance_date__gte=instance.application_id.leave_from,
            attendance_date__lte=instance.application_id.leave_to
        ).exists():
            if instance.application_id.is_approved:

                leave_from = instance.application_id.leave_from
                leave_to = instance.application_id.leave_to
                instances = [CompanyUserAttendance(
                            company_name=instance.mpo_name.company_name,
                            user_id=instance.mpo_name,
                            attendance_date=leave_from + timedelta(days=i),
                            month=month_number_to_name[(leave_from + timedelta(days=i)).month],
                            is_leave=True,
                            leave_type=instance.application_id.leave_type
                        ) for i in range((leave_to - leave_from).days + 1)]
                CompanyUserAttendance.objects.bulk_create(instances)


