from django.apps import AppConfig


class OtherrolesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'otherroles'

    def ready(self):
        import otherroles.signals
