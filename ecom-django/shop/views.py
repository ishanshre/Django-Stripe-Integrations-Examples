from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from shop.models import Cart, CartItem, Order, OrderItem


# Create your views here.
class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = "cart.html"
    context_object_name = "cart"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return Cart.objects.get_or_create(user=self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
