from django.apps import AppConfig


class StockistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Stockist'
    # def ready(self):
    #     import Stockist.signals
