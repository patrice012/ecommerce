import django_filters

from .models import Product

class ProductFilter(django_filters.FilterSet):
        # name = django_filters.CharFilter(lookup_expr='icontains' and 'istartswith')

        class Meta:
            model = Product
            fields = {
                'name': ['icontains'],
                'price': ['lt', 'gt'],
                # 'create': ['exact', 'year__gt'],
            }

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     print(dict(self.filters)['name__icontains'].field_class.hidden_widget,'cccccccccccccccc')
        #     print(dir(dict(self.filters)['name__icontains'].field_class),'aaaaaaaaaaaaaaaaa')

        # @property
        # def qs(self):
        #     parent_qs = super().qs
        #     return parent_qs.filter(available=True)