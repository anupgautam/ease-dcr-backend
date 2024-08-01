from django.db.models.signals import post_save
from django.dispatch import receiver

from Company.models import Company
from Stat.models import CompanyDCRTourPlanValidity


@receiver(post_save, sender=Company)
def save_notices(sender, instance, created, **kwargs):
    if created:
        CompanyDCRTourPlanValidity.objects.create(
           company=instance,
           days=1 
        )