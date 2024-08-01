from django.apps import AppConfig


class DailycallrecordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dailycallrecord'

    def ready(self):
        import dailycallrecord.signals

