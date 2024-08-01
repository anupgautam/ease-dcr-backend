import string
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.db.models import Q
from django.apps import apps


class CreateQQuery:
    
    def __init__(self, query_lookup: str, field_list: list, query_value: str):
        self.query_lookup = query_lookup
        self.field_list = field_list
        self.query_value = query_value

    def create(self):
        Qr = None
        for field in self.field_list:
            q = Q(**{f"{field}__{self.query_lookup}": self.query_value})
            if Qr:
                Qr = Qr | q
            else:
                Qr = q
        return Qr


class Search:

    class Meta:
        abstract = True

    def search(self):
        pass


class TrigramSearch(Search):

    def __init__(self, query: str, model_name: str, field_list: list, app_name: str) -> None:
        self.query = query
        self.model_name = model_name
        self.field_list = field_list
        self.app_name = app_name
        self.similarity_index = 0.1

    def get_trigram_similarity(self):
        return_trigram = ()
        for field in self.field_list:
            return_trigram += (TrigramSimilarity(field, self.query),)
        return return_trigram

    def search(self):
        model = apps.get_model(self.app_name, self.model_name)
        trigram = self.get_trigram_similarity()
        query = CreateQQuery('trigram_similar', self.field_list, self.query).create()
        return (model.objects
                    .annotate(  
                        similarity=Greatest(*trigram))
                        .filter(query, similarity__gt=self.similarity_index)).order_by('-similarity')


class CompanyWiseTrigramSearch(Search):
    
    def __init__(self, query: str, model_name: str, field_list: list, app_name: str, company_id:int) -> None:
        self.query = query
        self.model_name = model_name
        self.field_list = field_list
        self.app_name = app_name
        self.similarity_index = 0.1
        self.company_id = company_id

    def get_trigram_similarity(self):
        return_trigram = ()
        for field in self.field_list:
            return_trigram += (TrigramSimilarity(field, self.query),)
        return return_trigram

    def search(self):
        model = apps.get_model(self.app_name, self.model_name)
        trigram = self.get_trigram_similarity()
        query = CreateQQuery('trigram_similar', self.field_list, self.query).create()
        return (model.objects
                    .annotate(  
                        similarity=Greatest(*trigram))
                        .filter(query, similarity__gt=self.similarity_index,
                                company_name__company_id = self.company_id)).order_by('-similarity')
    

class UserWiseTrigramSearch(Search):

    def __init__(self, query: str, model_name: str, field_list: list, app_name: str, user_id:int) -> None:
        self.query = query
        self.model_name = model_name
        self.field_list = field_list
        self.app_name = app_name
        self.similarity_index = 0.1
        self.user_id = user_id

    def get_trigram_similarity(self):
        return_trigram = ()
        for field in self.field_list:
            return_trigram += (TrigramSimilarity(field, self.query),)
        return return_trigram

    def search(self):
        model = apps.get_model(self.app_name, self.model_name)
        trigram = self.get_trigram_similarity()
        query = CreateQQuery('trigram_similar', self.field_list, self.query).create()
        return (model.objects
                    .annotate(  
                        similarity=Greatest(*trigram))
                        .filter(query, similarity__gt=self.similarity_index,
                                mpo_name = self.user_id)).order_by('-similarity')





