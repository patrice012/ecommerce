
from django.urls import path

from .views import (
            # checkout,
            CheckoutCreate,
)


app_name = "checkout"
urlpatterns = [
    path('', CheckoutCreate.as_view(), name = 'checkout'),
    # path('c', checkout, name = 'c_checkout'),
]