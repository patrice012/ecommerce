from django.contrib import admin

# Register your models here.
from .models import Checkout

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company', 'contry', 'address', 'postal_code', 'phone', 'email')
    search_fields = ('name','address','contry')
    # filter_horizontal = ('contry','contry')
# admin.site.register(Checkout)

admin.site.register(Checkout, CheckoutAdmin)
