from django.urls import path
from .views import (
    home,
    success,
    cancel,
    stripe_webhook,
    purchase_credits,
    create_checkout_session,
)

urlpatterns = [
    path('', home, name='transactions'),
    path('purchase-credits/', purchase_credits, name='purchase-credits'),
    path('create-checkout-session/', create_checkout_session,
         name='create-checkout-session'),
    path('cancel/', cancel, name='cancel'),
    path('success/', success, name='success'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]
