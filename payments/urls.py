from .views import (
    SuccessView,
    CancelView,
    stripe_webhook,
    purchase_credits,
    create_checkout_session,
)
from django.urls import path
from payments import views


urlpatterns = [
    path('purchase-credits/', purchase_credits, name='purchase-credits'),
    path('create-checkout-session/', create_checkout_session,
         name='create-checkout-session'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]
