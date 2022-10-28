
from django.urls import path

from .views import (
            auth_login,
            auth_logout,
            auth_register,
            auth_change_password,
)


app_name = "authapp"
urlpatterns = [
    path('login/', auth_login, name ='login'),
    path('logout/', auth_logout, name ='logout'),
    path('register/', auth_register, name ='register'),
    path('change-password/', auth_change_password, name ='change_password'),
]