import json
from datetime import timezone
from django.core import serializers
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
    user = request.user
    try:
        cart = Cart.objects.get(cart_user = user.id, complete=False)
    except:
        
        return JsonResponse({})
# if cart:
    cart_item = cart.cartitem_set.all()
    product = [{
        'name': cart_product.product.name,
        'quantity': cart_product.product_quantity,
        'price': cart_product.product.price,
        'imgUrl': cart_product.product.image_url}
        for cart_product in cart_item]

    cart_item_number = cart_item.count()
    return JsonResponse({'cart_item_number':cart_item_number, 'product':product}, status = 200)
# return render(request, 'product/index.html')



@login_required
def cart(request):
    cart, cart_item = {}, {}
    try:
        cart = Cart.objects.get(cart_user = request.user, complete=False)
        cart_item = cart.cartitem_set.all()
    except:
        pass
        # but send message to say to the user that his cart is empty

    context = {
        'cart': cart,
        'cart_item': cart_item,
    }
    return render(request, 'cart/cart.html', context)



def add_to_cart(request):
    user = request.user
    # try:
    cart, created = Cart.objects.get_or_create(cart_user = user, complete=False)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.load(request)
        product_number = data.get('productNumber')
        product_name = data.get('name')
        product_id = data.get('id')

        # product = Product.objects.get(name=product_name, id=product_id)
        product = get_object_or_404(Product, id = product_id)

        cart_item, created = CartItem.objects.get_or_create(cart_id = cart, product = product)

        if cart:
            item =cart.cartitem_set.all().filter(product__id = product.id)
            if item:
                cart_item.product_quantity += int(product_number)
                cart_item.save()
            else:
                cart_item.product_quantity = int(product_number)
                cart_item.cart.cart_user = request.user
                cart_item.save()
        else:
            transaction_id = timezone.now()
            cart = Cart(cart_user = user, transaction_id = transaction_id )
            cart.cartitem_set.add(cart_item)

        msg = f'{product} was added to cart {cart} by {user}'
        sys_loggin('info',True, msg)
        # except:

    # context = {
    #     'cart_item':cart.cartitem_set.all(),
    # }
    # return render(request, 'cart/cart.html', context)

    return JsonResponse({'message':f'{product.name} was added successfully'}, status = 200)



def cart_action(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.load(request)
        cart = Cart.objects.get(cart_user = request.user.id, complete=False)
        cart_item = cart.cartitem_set.filter(product__id = data.get('id')).first()
        quantity = 0
        try:
            if data.get('action') == 'increase':
                cart_item.product_quantity += 1
                cart_item.save()

            elif data.get('action') == 'decrease':
                if ( cart_item.product_quantity  > 1): 
                    cart_item.product_quantity -= 1
                    cart_item.save()

                else:
                    cart_item.product_quantity = 0
                    msg = f'{cart_item} was deleted in the cart {cart} by {request.user}'
                    sys_loggin('info',True, msg)
                    cart_item.delete()
                    cart.save()
            # 
            quantity = cart_item.product_quantity
            price= cart_item.cart_item_total_cost
        except AttributeError:
            print('AttributeError')
        #     print()

        return JsonResponse({'quantity':quantity, 'price': price, 'cart_total': 0, 'cart_sub_total': cart.cart_total_cost}, status = 200)


    return render(request, 'cart/cart.html')


