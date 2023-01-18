from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


import time
import stripe

from core.models import UserPayment
# Create your views here.


@login_required
def product_page(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    if request.method == "POST":
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [
                {
                    "price": "price_1MRXwAA84iYHTQpxc4Q1h43A",
                    "quantity":2,
                },
            ],
            mode = 'payment',
            customer_creation = 'always',
            success_url = settings.REDIRECT_DOMAIN + "/payment/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = settings.REDIRECT_DOMAIN + "/payment/canceled",
        )
        return redirect(checkout_session.url, code = 303)
    context = {}
    return render(request, "product_page.html", context)


def payment_successfull(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.id
    user_payment = UserPayment.objects.get(user = request.user)
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.save()
    return render(request, 'payment_successfull.html', {"customer":customer})


def payment_canceled(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    return render(request, 'payment_canceled.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE-SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_KEY
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)
