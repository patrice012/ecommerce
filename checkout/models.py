from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Checkout(models.Model):
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    company = models.CharField(_("Company name"), max_length=50)
    contry = models.CharField(_("Contry /  Region"), max_length=50)
    city = models.CharField(_("City /  Team"), max_length=50)
    address = models.CharField(_("Street address"), max_length=50)
    postal_code = models.CharField(_("Postal code / ZIP"), max_length=50)
    phone = models.CharField(_("Phone number"), max_length=254)
    email = models.EmailField(_("Email"), max_length=254)

    notes = models.TextField(_("Order notes (optional)"), blank=True, null=True)

    def __str__(self):
        return self.first_name + self.company


# class Payment(modals.Modal):
#     stripe = 
