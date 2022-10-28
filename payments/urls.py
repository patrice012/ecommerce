# payments/urls.py

from django.urls import path

from . import views

app_name='payments'
urlpatterns = [
    # path('', views.HomePageView.as_view(), name='home'),
    # path('config/', views.stripe_config),  # new

    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe_webhook'),

    path('create-payment-intent/<pk>/', views.StripeIntentView.as_view(), name='create-payment-intent'),
    path('custom-payment/', views.CustomPaymentView.as_view(), name='custom-payment')
]
