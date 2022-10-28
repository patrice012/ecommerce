from django import forms

from .models import Product

# use in django admin to create a product
class ProductForm(forms.ModelForm):
    # product_image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model = Product
        fields = ['name', 'price', 'discount_price', 'short_description', 'long_description', 'quantity_in_stock', 'available', 'product_type','product_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_image'].widget.attrs.update({'multiple':True})
        # self.fields['product_image'].widget=forms.ClearableFileInput