import json
from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.models import Product
from shop.models import Cart, CartItem, Order, OrderItem


# Create your views here.
class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = "cart.html"
    context_object_name = "cart"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return Cart.objects.prefetch_related("cart_items__product").get_or_create(
            user=self.request.user
        )[0]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


@login_required()
def add_to_cart(request):
    if request.method == "POST":
        cart, created = Cart.objects.get_or_create(user=request.user)
        data = json.loads(request.body)
        product_id = data.get("product_id", None)
        if product_id is None or product_id == "":
            return JsonResponse(
                {
                    "message": "Provide product id",
                },
                status=400,
            )
        product = Product.objects.get(id=int(product_id))
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if cart_item.quantity:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1
        cart_item.save()
        return JsonResponse(
            {
                "message": "Product added to cart",
            },
            status=200,
        )
    else:
        return JsonResponse(
            {
                "message": f"Method {request.method} not allowed",
            },
            status=405,
        )


@login_required()
def delete_item(request, product_id):
    cart = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=int(product_id))
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return JsonResponse(
        {
            "message": "Product deleted from cart",
        },
        status=200,
    )
