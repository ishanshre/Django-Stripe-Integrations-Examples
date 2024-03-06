from django.urls import path

from shop import views

app_name = "shop"


urlpatterns = [
    path("cart/", views.CartDetailView.as_view(), name="cart-view"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
]
