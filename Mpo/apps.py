from django.apps import AppConfig


class MpoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Mpo'
    def ready(self):
        import Mpo.signals
