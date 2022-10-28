import json
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, DetailView,DeleteView, UpdateView, ListView)

from .models import Product, File
from .forms import ProductForm


def search(request):
    title = ''
    search_product = []
    if request.method == "GET":
        query = request.GET.get('q')

        # product = Product.objects.all()
        product= Product.is_available.all()
        print(product)
        search_by_price = product.filter( 
            Q(price__iexact=str(query)))
        title_price = 'Price'
        search_by_name = product.filter(
            Q(name__icontains=str(query)))
        title_name = 'Name'
        search_by_author = product.filter(
            Q(by_user__icontains=str(query)))
        title_author = 'Author'

    context = {
        'search_by_name': search_by_name,
        'title_name': title_name,
        'search_by_price': search_by_price,
        'title_price': title_price,
        'search_by_author': search_by_author,
        'title_author':title_author,
        'query':query,
    }
    return render(request, 'product/search.html', context)
    # return redirect('product:search_result')


def home(request):
    # get tree random products by using order_by('?')
    # product = Product.objects.all().order_by('?')[:3]
    product= Product.is_available.all().order_by('?')[:3]
    context = {
        'product': product,
    }
    return render(request, 'product/index.html', context)


class CreateProduct(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/create_update_product.html"
    # success_message = "%(name)s was created successfully"
    success_message = "was created successfully"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('product_image')
        file_list = []
        if form.is_valid():
            for file in files:
                product_file = File(product_file = form.instance, file=file)
                form.instance.save()
                product_file.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        form.instance.by_user = str(self.request.user)
        form.save()
        return redirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create product"
        return context
    

class UpdateProduct(LoginRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product/create_update_product.html"

    def form_valid(self,form):
        form.instance.by_user = str(self.request.user)
        form.save()
        return redirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update product"
        return context



class ProductList(ListView):
    model = Product
    template_name = 'product/product_list.html'
    paginate_by = 9

    def  get_queryset(self):
        return super().get_queryset().order_by('?')
    


class DeleteProduct(LoginRequiredMixin, DeleteView):
    model = Product
    # template_name = 'product/delete_product.html'
    success_url = reverse_lazy('dashboard:dashboard')


def product_detail(request, name, id,price):
    product = Product.objects.get(name = name, id = id, price = price)
    # pr = File.objects.filter(product_file = product)
    # print(product.by_user)
    # print(request.user)
    # cart = Cart.objects.get(cart_user = request.user, complete=False).cartitem_set.all()
    # print(cart, 'caaaaaaaaaaaaaaaaaaaaaa')
    # cart_item = cart.cartitem_set.all()
    # if product.by_user == request.user:
    #     print('hhhhhhhhhhhhhh')
    product_file = product.file_set.all()
    main_image = product_file.first()
    gallery = product_file.order_by('?')[1:]
    context = {
        'product': product,
        'main_image': main_image,
        'gallery': gallery,
    }
    return render(request, 'product/product_detail.html', context)
