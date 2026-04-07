from django.apps import AppConfig

class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    def ready(self):
        from django.conf import settings
        settings.HANDLER403 = 'tracker.views.custom_403'