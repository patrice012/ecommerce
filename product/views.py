import random

from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView,
                                  UpdateView)
from django.views.generic.base import TemplateView

from product.loggin_mixin import sys_loggin
from .filters import ProductFilter
from .forms import ProductForm
from .models import File, Product


def search(request):
    title = ''
    search_product = []
    if request.method == "GET":
        query = request.GET.get('q')

        # product = Product.objects.all()
        product = Product.is_available.all()
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
        'title_author': title_author,
        'query': query,
    }
    return render(request, 'product/search.html', context)
    # return redirect('product:search_result')


def randint(qs) -> int:
    randint = random.randint(1, qs.count())
    return randint


def home(request):
    per = request.user.get_user_permissions(obj=None)
    print(per, 'permission fot the current user')
    qs = Product.is_available.all()
    try:
        offer = qs.get(id=randint(qs))
    except:
        offer = qs.get(id=randint(qs))
    product = qs.order_by('?')[:3]
    context = {
        'product': product,
        'offer': offer
    }
    return render(request, 'product/index.html', context)


class CreateProduct(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/create_update_product.html"
    # success_message = "%(name)s was created successfully"
    permission_required = 'product.add_product'
    success_message = "was created successfully"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('product_image')
        file_list = []
        if form.is_valid():
            for file in files:
                product_file = File(product_file=form.instance, file=file)
                form.instance.save()
                product_file.save()
                msg = f'{form.instance} was created by {form.instance.by_user}'
                sys_loggin('info', True, msg)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.by_user = str(self.request.user)
        form.save()
        return redirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create product"
        return context


class UpdateProduct(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'product.change_product'
    template_name = "product/create_update_product.html"

    def post(self, *args, **kwargs):
        msg = f'{self.get_object()} was updated by {self.request.user}'
        sys_loggin('info', True, msg)
        return super().post(*args, **kwargs)

    def form_valid(self, form):
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

    def get_queryset(self):
        dict_request = dict(self.request.GET)
        if dict_request:
            for i, lookup in enumerate(dict_request):
                if dict_request[lookup][0] != ['']:
                    return ProductFilter(self.request.GET, queryset=Product.objects.all()).qs
        return super().get_queryset().order_by('?')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.add_message(self.request, messages.INFO, 'Hello world.')
        context["filter"] = ProductFilter()
        return context

        #  f = ProductFilter(self.request.GET, queryset=Product.objects.all())


class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product

    def post(self, *args, **kwargs):
        msg = f'{self.get_object()} was deleted by {self.request.user}'
        sys_loggin('info', True, msg)
        return super().post(*args, **kwargs)
    success_url = reverse_lazy('dashboard:dashboard')


@login_required()
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    msg = f'{product} was deleted by {request.user}'
    if request.user.has_perm('product.delete_product'):
        product.delete()
    else:
        product.is_deleted = True
    sys_loggin('warning', True, msg)
    return redirect(reverse('dashboard:dashboard'))


def product_detail(request, name, id, price):
    product = Product.objects.get(name=name, id=id, price=price)
    product_file = product.file_set.all()
    main_image = product_file.first()
    gallery = product_file.order_by('?')[1:]
    context = {
        'product': product,
        'main_image': main_image,
        'gallery': gallery,
    }
    return render(request, 'product/product_detail.html', context)


class ContactView(TemplateView):
    template_name = "product/contact.html"
