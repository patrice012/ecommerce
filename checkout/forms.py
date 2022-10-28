from django import forms
from .models import Checkout

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = fields = ['first_name', 'last_name', 'company', 'contry', 'city', 'address', 'postal_code', 'phone', 'email']