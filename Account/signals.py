from django.db.models.signals import post_save
from django.dispatch import receiver

from Account.models import User
from DCRUser.models import (CompanyUserRole,
                            Company,
                            CompanyUser)
from Company.models import Roles


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
        if created:
            company_name = Company.objects.get(
                    company_id=instance.company_name
                )
            if instance.role_name is not None:
                user_role = Roles.objects.get(
                    role_id=instance.role_name
                )
                company_user_role = CompanyUserRole(
                    role_name=user_role,
                    company_name=company_name,
                    user_name=instance
                )
                company_user_role.save()
            if instance.company_name is not None:
                company_user = CompanyUser(
                    company_name = company_name,
                    user_name =instance
                )
                company_user.save()

