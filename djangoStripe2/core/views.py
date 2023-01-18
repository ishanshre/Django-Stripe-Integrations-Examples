from django.shortcuts import render
from django.views.generic import ListView, DetailView

from core.models import Product

import stripe

# Create your views here.


class IndexView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = "index.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/detail.html'
