from django.contrib import admin
from shop.models import Order, OrderItem, Cart, CartItem

# Register your models here.


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
