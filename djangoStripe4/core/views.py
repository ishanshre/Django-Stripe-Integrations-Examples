from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from core.models import Product
# Create your views here.
class IndexView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = "index.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/detail.html'


class SuccessView(TemplateView):
    template_name = "payment/success.html"

class CancelView(TemplateView):
    template_name = "payment/cancel.html"

