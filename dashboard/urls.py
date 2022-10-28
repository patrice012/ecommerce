
from django.urls import path

from .views import dashboard, profile, update_profile



app_name = 'dashboard'
urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('profile', profile, name="profile"),
    path('profile/update', update_profile, name="update-profile"),
]