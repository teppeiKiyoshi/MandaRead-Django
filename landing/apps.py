from django.apps import AppConfig


class LandingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landing'

    # Importing Signals (When user registered, create new profile)
    def ready(self):
        import landing.signals
