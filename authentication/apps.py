from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'authentication'
    verbose_name = 'Authentication'

    def ready(self):
        import authentication.signals

default_app_config = 'backend.apps.authentication.AuthenticationConfig'