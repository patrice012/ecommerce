from django.db import models
from django.utils.translation import gettext_lazy as _


class DateMixin(models.Model):
    create = models.DateTimeField(_("Cart created at"), auto_now_add=True)
    update = models.DateTimeField(_("cart updated at"), auto_now=True)

    class Meta:
        abstract=True