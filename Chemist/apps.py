from django.apps import AppConfig


class ChemistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Chemist'
    def ready(self):
        import Chemist.signals
