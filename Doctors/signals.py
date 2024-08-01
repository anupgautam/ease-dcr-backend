from django.db.models.signals import post_save
from django.dispatch import receiver

from Doctors.models import *
from Company.models import Company


@receiver(post_save, sender=Doctor)
def save_doctor(sender, instance, created, **kwargs):
    if created:
        # try:
        #     field = MyModel._meta.get_field(field_name)
        # except MyModel._meta.get_field.DoesNotExist:
        company_name = Company.objects.get(company_id=instance.company_name)
        mpo_name = CompanyUserRole.objects.get(id=instance.mpo_name)
        # category_name = CompanyDoctorCategory.objects.get(id=instance.category_name)
        company_doctor = CompanyWiseDoctor(doctor_name=instance,
                                            company_name=company_name,
                                            mpo_name=mpo_name,
                                            is_investment=instance.is_investment)
        # doctor_category = CategoryWiseDoctor(doctor_category=category_name,
        #                                     doctor_name=instance)
        # doctor_category.save()
        company_doctor.save()
    # else:
    #     doctor = Doctor.objects.get(id=instance.id)
    #     doctor.save()
        # updated_category_name = CompanyDoctorCategory.objects.get(
        #     id=instance.category_name)
        # category_wise_doctor = CategoryWiseDoctor.objects.get(
        #     doctor_name=doctor) 
        # category_wise_doctor.doctor_category = updated_category_name
        # category_wise_doctor.save()



        