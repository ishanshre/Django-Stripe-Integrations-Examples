from django.contrib import admin
from core.models import Product, ProductTag, PaymentHistory
# Register your models here.


admin.site.register(Product)
admin.site.register(PaymentHistory)
admin.site.register(ProductTag)
