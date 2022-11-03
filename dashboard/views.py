from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, DetailView, ListView,UpdateView

from product.models import Product
from cart.models import Cart, CartItem
from .models import Profile
from .forms import UpdateProfileForm


User = get_user_model()

# Create your views here.
@login_required
def profile(request):

    try:
        user = User.objects.get(id = request.user.id)
        user_profile = Profile.objects.get(id = user.profile.id)
    except:
        user = ''
    context = {
        'user':user,
        'profile':user_profile
    }
    return render(request, 'dashboard/partials/_profile.html', context)

@login_required
def dashboard(request):
    context = {}
    try:
        user_profile = request.user.profile
    except:
        user_profile = request.user

    try:
        cart = cart = Cart.objects.get(cart_user = request.user, complete=False)
        cart_item = cart.cartitem_set.all()
        paginator = Paginator(cart_item, 5) # Show 5 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        return render(request, 'dashboard/dashboard.html', context)
    context = {
        'cart':cart,
        'cart_item':cart_item,
        'user':user_profile,
        'page_obj': page_obj,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def update_profile(request):
    profile = Profile.objects.get(id = request.user.profile.id )
    form = UpdateProfileForm( instance=profile)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard')
    context  = {
        'profile': profile,
        'form':form
    }
    return render(request, 'dashboard/update_profile.html', context)


class ProductList(ListView):
    model = Product
    template_name = 'dashboard/partials/_product_list.html'
    paginate_by = 9

class ProductDetailView(DetailView):
    model = Product
    template_name = "dashboard/partials/_product_detail.html"
