from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from Product.models import CompanyProduct,Product,CompanyDivisionProduct
from Company.models import Company


@receiver(post_save, sender=Product)
def save_product(sender, instance, created, **kwargs):
    if created:
        
        company_name = Company.objects.get(
            company_id=instance.company_name)
        
        companyproduct = CompanyProduct(
            company_name=company_name,
            product_name=instance
        )
        companyproduct.save()

        
