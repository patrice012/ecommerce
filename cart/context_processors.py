from django.shortcuts import get_object_or_404

from .models import Cart, CartItem


def context_cart_item(request):
    cart_item, cart_item_number = CartItem.objects.none(), 0
    if request.user.is_authenticated:
        try:
            cart = get_object_or_404(Cart, cart_user=request.user, complete=False)
            # cart = Cart.objects.get(cart_user=request.user, complete=False)

            cart_item = cart.cartitem_set.all()
            cart_item_number = cart_item.count()
        except:
            pass
    context = {
        'context_cart_item': cart_item,
        'cart_item_number': cart_item_number,
    }
    return context
