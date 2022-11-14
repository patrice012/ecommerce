from django.db import models
from django.utils import timezone
from django.shortcuts import redirect, render, reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .utils import upload_to, user_directory_path
from .managers import ProductManager

# Create your models here.

User = settings.AUTH_USER_MODEL

TYPE = (
    ('physic', 'Physic'),
    ('numeric', 'Numeric'),
    ('book', 'Book'),
    ('download_prod', 'Download Product',)
)


class Product(models.Model):
    create = models.DateTimeField(auto_now_add=True)
    by_user = models.CharField(_("User"), max_length=50, null=True, blank=True)
    name = models.CharField(_("Product name"), max_length=50)
    price = models.PositiveIntegerField(_("Price"))
    discount_price = models.PositiveIntegerField(_("Discount price"), default=0, blank=True)
    short_description = models.CharField(_("Short description"), max_length=50, null=True, blank=True)
    long_description = models.TextField(_("Long description"), null=True, blank=True)
    quantity_in_stock = models.PositiveIntegerField(_("Quantity"), default=1, blank=True)
    available = models.BooleanField(_("Available"), default=True)
    product_type = models.CharField(_("Type of product"), choices=TYPE, max_length=50, null=True, blank=True)
    product_image = models.ImageField(_("Product Gallery"))
    is_deleted = models.BooleanField(default=False)

    # url = models.URLField()

    objects = models.Manager()
    is_available = ProductManager()

    def __str__(self):
        return str(self.name)

    @property
    def image_url(self):
        try:
            url = self.product_image.url
        except:
            url = ''
        return url

    @property
    def product_finaly_price(self):
        return int(self.price) - int(self.discount_price)

    def get_absolute_url(self):
        kwargs = {
            'name': self.name,
            'id': self.id,
            'price': self.price,
        }
        return reverse("product:product-detail", kwargs=kwargs)

    # @property
    # def product_images(self):
    #     images = self.file_set.all()
    #     return images


class File(models.Model):
    product_file = models.ForeignKey(Product, verbose_name=_("Product files"), on_delete=models.CASCADE)
    file = models.ImageField(_("Product Gallery"), upload_to=user_directory_path)

    def __str__(self):
        return str(self.file)

    @property
    def file_url(self):
        try:
            url = self.file.url
        except:
            url = ''
        return url
