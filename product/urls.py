from django.urls import path

from .views import (
    home, product_detail, CreateProduct,
    UpdateProduct, DeleteProduct, ProductList, search,
    ContactView, delete_product
)

app_name = "product"
urlpatterns = [
    path('<str:name>/<int:id>/<int:price>/', product_detail, name='product-detail'),
    path('update/<int:pk>/', UpdateProduct.as_view(), name="update-product"),
    # path('delete/<int:pk>/', DeleteProduct.as_view(), name="delete-product"),
    path('delete/<int:pk>/', delete_product, name="delete-product"),
    path('list/', ProductList.as_view(), name="product_list"),
    path('search/', search, name="search"),
    path('create/', CreateProduct.as_view(), name='create-product'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('', home, name='home'),
]
