from django.shortcuts import redirect, render,reverse, get_object_or_404
from django.views.generic import (
                            CreateView,UpdateView, ListView
                            )
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse

# Create your views here.
from cart.models import Cart, CartItem
from .models import Checkout
from .forms import CheckoutForm



# def checkout(request):
#     return render(request, 'checkout/checkout.html')


class CheckoutCreate(SuccessMessageMixin,CreateView):
    model = Checkout
    fields = ['first_name', 'last_name', 'company', 'contry', 'city', 'address', 'postal_code', 'phone', 'email']
    # form_class = CheckoutForm
    template_name = 'checkout/checkout.html'


    def form_valid(self, form):
        data = self.request.POST
        if data['order_notes']:
            form.instance.notes = data['order_notes']
            success_message="Information was send successfully"
        if 'payment' in data:
            payment_type = data['payment']

        form.instance.payment = payment_type
        form.save()
        return redirect(reverse('payments:create_checkout_session'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(cart_user = self.request.user.id, complete=False)
        cart_item = cart.cartitem_set.all()
        context["cart_item"] = cart_item
        context["cart"] = cart
        return context

        

    def form_invalid(self, form):
        success_message = "Error try again"
