from django.db import models
class Search:

    def __init__(self, queryset) ->None:
        self.queryset = queryset

    def get_model_name(self):
        return self.queryset.model.__name__

    def get_fields(self, model):
        return [ f.name for f in self.queryset.model._meta.fields
         + self.queryset.model._meta.many_to_many ]
    
    def get_app_name(self):
        return self.queryset.model._meta.app_label
    
    def get_field_list(self):
        field_lists = self.get_fields(model=self.queryset.model)
        new_tuple_1 = tuple(
        item for item in field_lists if item != 'id'
        )
        return new_tuple_1
            