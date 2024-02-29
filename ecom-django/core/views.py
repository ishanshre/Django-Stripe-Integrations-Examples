from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings

from core.models import Product


# Create your views here.
class IndexView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "index.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "product/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stripe"] = settings.STRIPE_PUBLIC_KEY
        return context


class SuccessView(TemplateView):
    template_name = "payment/success.html"


class CancelView(TemplateView):
    template_name = "payment/cancel.html"
