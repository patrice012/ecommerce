from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.





def cart(request):
    return render(request, 'deliver/cart.html')

def checkout(request):
    return render(request, 'deliver/checkout.html')