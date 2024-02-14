from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from cart.cart import Cart
from cart.forms import CheckOutForm

from core.models import Order, OrderItem

from django.conf import settings
import json
import stripe
# Create your views here.

@login_required
def add_to_cart(request, pk):
    cart = Cart(request)
    cart.add(product_id=pk)
    return redirect('core:index')

@login_required
def cart_view(request):
    return render(request, "cart/cart_view.html")


@login_required
def cart_update(request, pk, action):
    cart = Cart(request)
    if action == 'decrement':
        cart.update(product_id=pk, quantity=-1, update_quantity=True)
    if action == 'increment':
        cart.update(product_id=pk, quantity=1, update_quantity=True)
    return redirect('core:cart_view')


class CheckOutView(LoginRequiredMixin, View):
    template_name = 'cart/checkout.html'
    stripe_pub_key = settings.STRIPE_PUBLIC_KEY
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"stripe_pub_key":self.stripe_pub_key})

@login_required
def start_order(request):
    cart = Cart(request)
    print(cart)
    data = json.loads(request.body)
    total_price = 0
    items = []
    """Creating a list of product items for stripe checkout session"""
    for item in cart:
        print("item", item)
        product = item['product']
        quantity = int(item['quantity'])
        total_price += product.price * quantity
        obj = {
            "price_data":{
                "currency":"npr",
                "product_data":{
                    "name": product.name,
                    "description": product.body,
                    "images": [
                        request.build_absolute_uri(product.thumbnail.url),
                    ],
                },
                "unit_amount": int(product.price) * 100
            },
            "quantity":quantity
        }
        items.append(obj)
    
    
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    session = stripe.checkout.Session.create(
        line_items = items,
        mode = "payment",
        customer_creation = 'always',
        success_url = settings.PAYMENT_SUCCESS_URL,
        cancel_url = settings.PAYMENT_CANCEL_URL,
    )
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    zipcode = data["zipcode"]
    place = data["place"]
    phone = data["phone"]
    address = data["address"]
    order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            zipcode=zipcode,
            place=place,
            phone=phone,
            address=address,
            stripe_id=session.stripe_id,
            paid=True,
            paid_amount=total_price
        )
    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price = product.price * quantity
        item = OrderItem.objects.create(
            order=order,
            product=product,
            price=price,
            quantity=quantity
        )
    cart.clear()
    return JsonResponse({"sessionId":session.id})
        

