from django.db.models.signals import post_save
from django.dispatch import receiver

from Company.models import Notices, Company, CompanyNotices


@receiver(post_save, sender=Notices)
def save_notices(sender, instance, created, **kwargs):
    if created:
        company_name = Company.objects.get(company_id=instance.company_name)
        company_notices = CompanyNotices(
            company_name=company_name, notice_name=instance
        )
        company_notices.save()
