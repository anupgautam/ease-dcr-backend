from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from Stockist.models import Stockist, CompanyStockist
from Company.models import Company
from rest_framework.response import Response

# @receiver(post_save, sender=Stockist)
# def save_stockist(sender, instance, created, **kwargs):
#     if created:
#         
#         
#         stockist_company = Company.objects.get(
#                                 company_id=instance.company_name)
#         
#         company_stockist = CompanyStockist(
#                                 company_name=stockist_company,
#                                 stockist_name=instance)
#         company_stockist.save()


# @receiver(post_delete, sender=CompanyStockist)
# def delete_stockist(sender, instance, **kwargs):
#     stockist_instance = Stockist.objects.get(
#         id=instance.stockist_name.id
#         )
#     stockist_instance.delete()
#     return Response("data deleted successfully")
    
        