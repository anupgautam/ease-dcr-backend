from django.db.models.signals import post_save
from django.dispatch import receiver

from Chemist.models import *
from Company.models import Company


@receiver(post_save, sender=Chemist)
def save_chemist(sender, instance, created, **kwargs):
    if created:
        company_name = Company.objects.get(
            company_id=instance.company_name)
        mpo_name = CompanyUserRole.objects.get(
            id=instance.mpo_name
        )
        company_wise_chemist = CompanyWiseChemist(
            company_name=company_name,
            chemist_name=instance,
            mpo_name=mpo_name,
            is_investment=instance.is_investment
        )
        company_wise_chemist.save()
