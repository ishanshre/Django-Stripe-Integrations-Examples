from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

from core.models import Product
from shop.manager import ActiveManager

User = get_user_model()


# Create your models here.
class Order(models.Model):
    class PAYMENT_STATUS(models.TextChoices):
        PENDING = "P", "Pending"
        COMPLETE = "C", "Complete"
        FAILED = "F", "Failed"
        CANCELED = "CA", "Canceled"

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS.choices, default=PAYMENT_STATUS.PENDING
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    active = ActiveManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} --> order status --> {self.payment_status}"

    class Meta:
        permissions = [
            ("cancel_order", "Can cancel order"),
        ]


# Order Items
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name="order_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="product_orderitems"
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], blank=True
    )

    def save(self):
        self.unit_price = self.product.price * self.quantity
        return super().save()


class Cart(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, max_length=36
    )
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username


# cart items model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cartitems_product"
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    is_deleted = models.BooleanField(default=False)
    active = ActiveManager()
    objects = models.Manager()

    class Meta:
        unique_together = [["cart", "product"]]
