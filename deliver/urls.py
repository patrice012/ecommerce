
from django.urls import path

from .views import (
            cart,
            checkout,
)


app_name = "deliver"
urlpatterns = [
    path('cart/', cart, name ='cart'),
    path('checkout/', checkout, name='checkout')
]
