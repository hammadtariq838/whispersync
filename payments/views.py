from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model
import stripe


from .models import Payment
from .forms import PaymentForm


stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()


@login_required
def home(request):
    payments = Payment.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'payments/home.html', {'payments': payments})


@login_required
def success(request):
    return render(request, 'payments/success.html')


@login_required
def cancel(request):
    return render(request, 'payments/cancel.html')


@login_required
def create_checkout_session(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        amount = int(float(amount) * 100)  # convert to cents
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
            success_url=settings.DOMAIN + '/payments/success/',
            cancel_url=settings.DOMAIN + '/payments/cancel/',
            metadata={
                'user_id': request.user.id,
                'amount': amount
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
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse("Signature verification failed", status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        amount = session['metadata']['amount']
        user = get_object_or_404(User, id=user_id)
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
