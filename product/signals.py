from django.core import signals
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Product


@receiver(pre_delete, sender=Product)
def delete_permis(instance, **kwargs):
    pass
