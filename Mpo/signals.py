import threading

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import ActiveWorkingDays
from .utils import get_dates_x_years
from Company.models import Company
 
 
def bulk_create_company_date(instance):
    date_list = get_dates_x_years(10)
    company_date_list = [
            ActiveWorkingDays(company=instance, date=i, is_holiday=False) for i in date_list 
        ]
    ActiveWorkingDays.objects.bulk_create(company_date_list)


def bulk_delete_company_date(instance):
    ActiveWorkingDays.objects.filter(company=instance.id).delete()


@receiver(post_save, sender=Company)
def create_company_date(sender, instance, created, **kwargs):
    if created:
        company_create_thread = threading.Thread(
            target=bulk_create_company_date(instance))
        company_create_thread.start()


@receiver(pre_delete, sender=Company)
def delete_company_date(sender, instance, **kwargs):
    company_delete_thread = threading.Thread(
        target=bulk_delete_company_date(instance)
    )
    company_delete_thread.start()