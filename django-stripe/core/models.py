from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save

# Create your models here.
class UserPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment")
    payment = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username

@receiver(signal=post_save, sender = User)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        payment = UserPayment.objects.create(user=instance)
        payment.save()
