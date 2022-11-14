
from django.urls import path

from .views import (
            add_to_cart,
            cart_item,
            cart,
            cart_action,
)


app_name = "cart"
urlpatterns = [
    path('i/', cart_item, name="cart-item"), 
    path('cart-action/', cart_action, name="cart_action"),
    path('cart/', cart, name='cart'),
    path('add/', add_to_cart, name="add-to-cart"),
]