from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout , authenticate
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.debug import sensitive_post_parameters


from product.loggin_mixin import sys_loggin

from .forms import (
                    UserCreationForm,
                    AuthenticationForm,
                    )

# Create your views here.
User = get_user_model()

@sensitive_post_parameters('email','password')
def auth_login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('email'), "ddddddddddddd")
            user = authenticate(request, email = form.cleaned_data.get('email'), password = form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                msg = f'{user} logging'
                sys_loggin('info', True, msg)
                # REDIRECT USER IF NEXT PARAMETER IS GIVEN ELSE REDIRECT TO THE DEFAULT PAGE
                if request.GET.get('next') is not None:
                    return redirect(request.GET['next'])
                return redirect('/')
    return render(request, "authapp/login.html", {'form':form})

def auth_register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            msg = f'{user} create account'
            sys_loggin('info', True, msg)
            return redirect('/')
        # else:
        #     form = UserCreationForm()
    context = {
        'form':form
    }
    return render(request, "authapp/register.html", context)

def auth_change_password(request):
    return render(request, "authapp/change_password.html")

def auth_logout(request):
    msg = f'{request.user} loggout'
    logout(request)
    sys_loggin('info', True, msg)
    return redirect('authapp:login')