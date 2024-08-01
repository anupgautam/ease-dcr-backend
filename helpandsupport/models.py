from django.db import models


class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    message = models.TextField()
