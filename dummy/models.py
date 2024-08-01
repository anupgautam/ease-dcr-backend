from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)

class City(models.Model):
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    places = models.CharField(max_length=200)
    