from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.db.models import Q

from .models import Chemist


from django.apps import apps
model_name = 'Chemist'
app_name = 'Chemist'
my_model = apps.get_model(app_name, model_name)


class Search(object):
    def __init__(self, query) -> None:
        self.query = query

    def search(self):
        return Chemist.objects.annotate(
                        similarity=Greatest(
                            TrigramSimilarity(
                                'chemist_name',
                                 self.query
                                 ),
                            TrigramSimilarity(
                                'chemist_address',
                                 self.query),
                            TrigramSimilarity(
                            'chemist_phone_number',
                             self.query),
                    )).filter(
                        Q(chemist_name__trigram_similar=self.query) |
                        Q(chemist_address__trigram_similar=self.query)
                        ,similarity__gt=0.1).order_by('-similarity')
