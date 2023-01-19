from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from core.models import Product, PaymentHistory

import stripe
import time
# Create your views here.

stripe.api_key = settings.STRIPE_PRIVATE_KEY


class IndexView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = "index.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/detail.html'



class StripeCheckOutSession(View):
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['pk'])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ["card"],
            line_items = [
                {
                    "price_data":{
                        "currency":"npr",
                        "unit_amount": int(product.price) * 100,
                        "product_data": {
                            "name":product.name,
                            "description":product.body,
                            "images": [
                                f"{settings.REDIRECT_DOMAIN}/{product.thumbnail.url}"
                            ],
                        },
                    },
                    "quantity":product.quantity
                }
            ],
            metadata={"product_id":product.id},
            mode="payment",
            success_url = settings.PAYMENT_SUCCESS_URL,
            cancel_url = settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "payment/success.html"

class CancelView(TemplateView):
    template_name = "payment/cancel.html"



@method_decorator(csrf_exempt, name='dispatch')
class StripeWebHook(View):
    def post(self,request, format=None, *args, **kwargs):
        time.sleep(10)
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_KEY
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)
        
        if event["type"] == "checkout.session.completed":
            print("payment success")
            session = event["data"]["object"]
            customer_email = session["customer_details"]["email"]
            product_id = session["metadata"]["product_id"]
            product = get_object_or_404(Product, id=product_id)
            payment = PaymentHistory.objects.create(
                email=customer_email,
                product = product,
                payment_status = "Completed",
            )
            payment.save()
        return HttpResponse(status=200)