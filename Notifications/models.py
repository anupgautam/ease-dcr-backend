from django.db import models
from Company.models import CompanyRoles, Company
from DCRUser.models import CompanyUser


class Notificaiton(models.Model):
    notification_title = models.TextField()
    notification_description = models.TextField()
    notification_date = models.DateField()
    company_name = models.ForeignKey(Company,
                                     on_delete=models.CASCADE)
    notificaiton_to = models.ForeignKey(CompanyRoles,
                                          on_delete=models.CASCADE,
                                          related_name='notification_to')
    notificaiton_from = models.ForeignKey(CompanyUser,
                                          on_delete=models.CASCADE,
                                          related_name='notification_from')


