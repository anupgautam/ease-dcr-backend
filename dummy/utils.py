from django.apps import apps
from django.db import models


def country_and_city_data_transmission(request):
    data = {
        "country":
        {
        "name": request.data.get('country_name'),
        "zip": request.data.get('zip'),
        "latitude": request.data.get('latitude'),
        "longitude": request.data.get('longitude'),
        },
        "name": request.data.get('city_name'),
        "places": request.data.get('places')
    }
    
    return data


# get the name of the foreign key field of model
def get_foreign_key_field_name(app_name, model_name):
    child_model = apps.get_model(app_name, model_name)
    foreign_key_field = child_model._meta.get_fields()
    foreign_key_fields = []
    for i in foreign_key_field:
        if isinstance(i,  models.ForeignKey):
            foreign_key_fields.append(i.name)
    return foreign_key_fields


def check_foreign_key(field):
    if field.is_relation:
        return True
    else:
        return False

def check_primary_key(field):
    if field.name=="id" or field.name=="uuid":
            return True
    else:
        return False


# get the name of all the fields excluding the foreign key fields
def fields_excluding_foreign_key(
    app_name, model_name):
    model = apps.get_model(app_name, model_name)
    fields = [field.name for field in model._meta.get_fields() if not check_foreign_key(field) and not check_primary_key(field)]
    
    return fields




