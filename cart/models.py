from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from product.models import Product

from .mixins import DateMixin

# Create your models here.

User = settings.AUTH_USER_MODEL

STATE = (
    ('pending', 'Pending'),
    ('success', 'Success'),
    ('cancel', 'Cancel'),
)


class Cart(DateMixin):
    cart_user = models.OneToOneField(User, verbose_name=_("Cart user"), on_delete=models.CASCADE)
    cart_state = models.CharField(_("Cart state"), choices=STATE, max_length=50, default="Pending")
    transaction_id = models.CharField(_("Transaction id"), max_length=100)
    complete = models.BooleanField(_("Complete cart"), default=False)

    def __str__(self):
        return str(self.cart_user) + str(self.id)

    @property
    def cart_total_cost(self):
        s = sum([cart_item.cart_item_total_cost for cart_item in self.cartitem_set.all()])
        return s


class CartItem(DateMixin):
    product = models.ForeignKey(Product, verbose_name=_("Cart product"), on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, verbose_name=_("Relate cart"), on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField(_("Cart item product"), default=0)
    cart_item_state = models.CharField(_("Product state"), choices=STATE, max_length=50)

    def __str__(self):
        return str(self.product)

    @property
    def cart_item_total_cost(self):
        return int(self.product.product_finaly_price) * int(self.product_quantity)
