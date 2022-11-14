from django.apps import AppConfig
from django.db.models.signals import post_save


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        from .signals import create_profile
        post_save.connect(create_profile, sender='authapp.User')
