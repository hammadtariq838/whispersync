from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Payment
from .forms import PaymentForm
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import stripe
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()


class SuccessView(TemplateView):
    template_name = "payments/success.html"


class CancelView(TemplateView):
    template_name = "payments/cancel.html"


def create_checkout_session(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        # convert to cents
        amount = int(float(amount) * 100)
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        else:
            domain = "https://yourdomain.com"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': amount,
                    'product_data': {
                        'name': 'Credits',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
            metadata={
                'user_id': request.user.id,
                'amount': amount,
            }
        )
        return redirect(checkout_session.url, code=303)


@login_required
def purchase_credits(request):
    form = PaymentForm()
    return render(request, 'payments/purchase_credits.html', {'form': form})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:  # invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        amount = session['metadata']['amount']
        user = User.objects.get(id=user_id)
        payment = Payment.objects.create(
            user=user,
            stripe_charge_id=session['payment_intent'],
            amount=amount
        )
        payment.save()
        user.profile.credits += int(amount)
        user.profile.save()

    # Since this view is called asynchronously, no redirect is necessary.
    return HttpResponse(status=200)
