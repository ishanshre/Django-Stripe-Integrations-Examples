from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.core.validators import MinValueValidator
from ckeditor.fields import RichTextField

# Create your models here.

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=255)
    body = RichTextField()
    thumbnail = models.ImageField(upload_to="product/image", blank=True)
    price = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:detail", args=[self.id])
