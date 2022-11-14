import json
from datetime import timezone
from django.db.models import Count, F
from django.forms import model_to_dict
# from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from product.loggin_mixin import sys_loggin
from product.models import Product

from .models import Cart, CartItem


# Create your views here.

@login_required
def cart_item(request):
    cart = get_object_or_404(Cart, cart_user=request.user.id, complete=False)
    cart_item = cart.cartitem_set.all()
    c = cart.cartitem_set.select_related('product')
    product_list = []
    for index, item in enumerate([product for product in c]):
        product_list.append(model_to_dict(item.product, fields=('name', 'quantity_in_stock', 'price')))
    cart_item_number = cart_item.count()
    return JsonResponse({'cart_item_number': cart_item_number, 'product': product_list}, status=200)


@login_required
def cart(request):
    cart = get_object_or_404(Cart, cart_user=request.user, complete=False)
    cart_item = cart.cartitem_set.all()
    context = {
        'cart': cart,
        'cart_item': cart_item,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(cart_user=user, complete=False)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.load(request)
        product_number = data.get('productNumber')
        product_name = data.get('name')
        product_id = data.get('id')
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(cart_id=cart, product=product)

        if cart:
            item = cart.cartitem_set.prefetch_related('product').filter(product__id=product.id)

            if item:
                cart_item.product_quantity = F('product_quantity') + int(product_number)
                cart_item.save()
            else:
                cart_item.product_quantity = int(product_number)
                cart_item.cart.cart_user = request.user
                cart_item.save()
        else:
            transaction_id = timezone.now()
            cart = Cart(cart_user=user, transaction_id=transaction_id)
            cart.cartitem_set.add(cart_item)

        cart_item.refresh_from_db()
        msg = f'{product} was added to cart {cart} by {user}'
        sys_loggin('info', True, msg)

    # context = {
    #     'cart_item':cart.cartitem_set.all(),
    # }
    # return render(request, 'cart/cart.html', context)

    return JsonResponse({'message': f'{product.name} was added successfully'}, status=200)


def cart_action(request):
    global price
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.load(request)
        cart = Cart.objects.get(cart_user=request.user.id, complete=False)
        cart_item = cart.cartitem_set.filter(product__id=data.get('id')).first()
        quantity = 0
        try:
            if data.get('action') == 'increase':
                cart_item.product_quantity = F('product_quantity') + 1
                cart_item.save()
                cart_item.refresh_from_db()

            elif data.get('action') == 'decrease':
                if cart_item.product_quantity > 1:
                    cart_item.product_quantity = F('product_quantity') - 1
                    cart_item.save()

                else:
                    cart_item.product_quantity = 0
                    msg = f'{cart_item} was deleted in the cart {cart} by {request.user}'
                    sys_loggin('info', True, msg)
                    cart_item.delete()
                    cart.save()
            #  refresh the database to update the last action because the use of F()
            quantity = cart_item.product_quantity
            price = cart_item.cart_item_total_cost
        except AttributeError:
            print('AttributeError')
        #     print()

        return JsonResponse(
            {'quantity': quantity, 'price': price, 'cart_total': 0, 'cart_sub_total': cart.cart_total_cost}, status=200)

    return render(request, 'cart/cart.html')
