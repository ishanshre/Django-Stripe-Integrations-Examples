from django.shortcuts import render, redirect

from cart.cart import Cart
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

