from django.contrib import admin

# Register your models here.
from .models import Product, File
from .forms import ProductForm

class ProductAdmin(admin.ModelAdmin):
    # add_form = ProductForm

    date_hierarchy = 'create'
    empty_value_display = '-empty-'
    list_display = ('name','by_user', 'price', 'discount_price', 'quantity_in_stock')

    search_fields = ('name', 'by_user')
    # filter_horizontal = ('price', 'name', 'by_user')

admin.site.register(Product, ProductAdmin)
admin.site.register(File)