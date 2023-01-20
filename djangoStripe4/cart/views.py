from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from cart.cart import Cart
from cart.forms import CheckOutForm

from core.models import Order, OrderItem
# Create your views here.


def add_to_cart(request, pk):
    cart = Cart(request)
    cart.add(product_id=pk)
    return redirect('core:index')


def cart_view(request):
    return render(request, "cart/cart_view.html")

def cart_update(request, pk, action):
    cart = Cart(request)
    if action == 'decrement':
        cart.update(product_id=pk, quantity=-1, update_quantity=True)
    if action == 'increment':
        cart.update(product_id=pk, quantity=1, update_quantity=True)
    return redirect('core:cart_view')


class CheckOutView(LoginRequiredMixin, View):
    template_name = 'cart/checkout.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

@login_required
def start_order(request):
    cart = Cart(request)
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        zipcode = request.POST.get("zipcode")
        place = request.POST.get("place")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            zipcode=zipcode,
            place=place,
            phone=phone,
            address=address
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
        
        return redirect("core:myaccount")
    return redirect('core:cart_view')

