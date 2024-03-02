from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView

from shop.models import Cart, CartItem, Order, OrderItem

# Create your views here.
