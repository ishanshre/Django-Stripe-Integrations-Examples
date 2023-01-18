from django.db import models
from django.urls import reverse

from django.core.validators import MinValueValidator
# Create your models here.

class ProductTag(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    tags = models.ManyToManyField(ProductTag, blank=True)
    body = models.TextField()
    thumbnail = models.ImageField(upload_to="product/image", blank=True)
    url = models.URLField()
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(decimal_places=2, max_digits=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} --> {self.price}"
    
    def get_absolute_url(self):
        return reverse("core:detail", args=[self.id])

