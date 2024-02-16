from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.core.validators import MinValueValidator

# Create your models here.

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=255)
    body = models.TextField()
    thumbnail = models.ImageField(upload_to="product/image", blank=True)
    url = models.URLField()
    price = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} --> {self.price}"

    def get_absolute_url(self):
        return reverse("core:detail", args=[self.id])


class Order(models.Model):
    ORDERED = "ordered"
    SHIPPED = "shipped"

    STATUS_CHOICES = ((ORDERED, "Ordered"), (SHIPPED, "Shipped"))

    user = models.ForeignKey(
        User, related_name="orders", blank=True, null=True, on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    stripe_id = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    class Meta:
        ordering = ("-created_at",)

    def get_total_price(self):
        if self.paid_amount:
            return self.paid_amount / 100

        return 0


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.price / 100
