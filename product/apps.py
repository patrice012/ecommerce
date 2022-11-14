from django.apps import AppConfig
from django.db.models.signals import pre_delete


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    def ready(self):
        from .signals import delete_permis
        pre_delete.connect(delete_permis, sender='product.Product')
