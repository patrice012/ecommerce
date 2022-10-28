import stripe
from django.shortcuts import redirect, render, reverse
from django.views.generic import TemplateView
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# payments/views.py

# from .models import Price

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        # price = Price.objects.get(id=self.kwargs["pk"])
        domain = "https://yourdomain.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            # line_items=[
            #     {
            #         'price': price.stripe_price_id,
            #         'quantity': 1,
            #     },
            # ],
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)




class SuccessView(TemplateView):
    template_name = "payment/success.html"

class CancelView(TemplateView):
    template_name = "payment/cancel.html"


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        # payment_intent = session["payment_intent"]

        line_items = stripe.checkout.Session.list_line_items(session["id"])
        # stripe_price_id = line_items["data"][0]["price"]["id"]
        # price = Price.objects.get(stripe_price_id=stripe_price_id)
        # product = price.product

        # TODO - send an email to the customer
        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. The URL is: {product.url}",
            recipient_list=[customer_email],
            from_email="your@email.com"
        )

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        price_id = intent["metadata"]["price_id"]

        price = Price.objects.get(id=price_id)
        product = price.product

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="your@email.com"
        )

    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            price = Price.objects.get(id=self.kwargs["pk"])
            intent = stripe.PaymentIntent.create(
                amount=price.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "price_id": price.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


class CustomPaymentView(TemplateView):
    template_name = "custom_payment.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        prices = Price.objects.filter(product=product)
        context = super(CustomPaymentView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context