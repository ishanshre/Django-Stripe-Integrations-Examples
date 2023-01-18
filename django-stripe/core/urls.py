from django.urls import path

from core import views


app_name = "core"

urlpatterns = [
    path('', views.product_page, name='product_page'),
    path('payment/success/', views.payment_successfull, name='payment_success'),
    path('payment/canceled/', views.payment_canceled, name='payment_canceled'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
]