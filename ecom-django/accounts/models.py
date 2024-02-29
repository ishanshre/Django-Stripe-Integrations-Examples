from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    phone = PhoneNumberField(null=True, blank=True, region="NP")
    zipcode = models.PositiveBigIntegerField(blank=True, null=True)
    shipping_address = models.CharField(max_length=128, blank=True, null=True)
    place = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.username
