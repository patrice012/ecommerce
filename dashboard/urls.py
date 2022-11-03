
from django.urls import path

from .views import dashboard, profile, update_profile,ProductList, ProductDetailView



app_name = 'dashboard'
urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('profile', profile, name="profile"),
    path('profile/update', update_profile, name="update-profile"),
    path('list/', ProductList.as_view(), name='dash_list'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='dash_detail'),
]