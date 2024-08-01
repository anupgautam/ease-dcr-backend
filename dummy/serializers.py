from rest_framework import serializers
from .models import *
from Doctors.description import Search
from .utils import (fields_excluding_foreign_key)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = City
        fields = '__all__'
    def create(self, validated_data):
        country_data = validated_data['country']
        parent_model = Search(Country.objects.all())
        parent_model_fields = (list(parent_model.get_field_list()))
        country_instance = Country(
        )
        for i in parent_model_fields:
            setattr(country_instance, i , country_data[i])
        country_instance.save()
        city_instance = City(
            country=country_instance,
        )
        child_model = Search(City.objects.all())
        child_model_fields = (list(child_model.get_field_list()))
        child_model_fields.remove('country')
        for j in child_model_fields:
            setattr(city_instance, j, validated_data[j])

        city_instance.save()
        return city_instance
    def update(self, instance, validated_data):
        country_data = validated_data['country']
        country_instance = instance.country
        parent_model_fields = fields_excluding_foreign_key(
            'dummy', 'Country')
        for i in parent_model_fields:
            setattr(country_instance, i , country_data[i])
        country_instance.save()
        child_model_fields = fields_excluding_foreign_key(
            'dummy', 'City'
        )
        for j in child_model_fields:
            setattr(instance, j, validated_data[j])
        instance.save()
        return instance