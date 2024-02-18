from django.urls import path
from django.contrib.auth.views import LogoutView

from core import views
from cart import views as cart_views
from accounts import views as user_views


app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/detail/", views.ProductDetailView.as_view(), name="detail"),
    path("success/", views.SuccessView.as_view(), name="success"),
    path("cancel/", views.CancelView.as_view(), name="cancel"),
    # urls for carts
    path("cart/add_to_cart/<int:pk>/", cart_views.add_to_cart, name="add_to_cart"),
    path("cart/view/", cart_views.cart_view, name="cart_view"),
    path(
        "cart/update/<int:pk>/<str:action>/", cart_views.cart_update, name="cart_update"
    ),
    path("checkout/", cart_views.CheckOutView.as_view(), name="checkout"),
    # urls for accounts
    path("login/", user_views.UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", user_views.UserRegisterView.as_view(), name="register"),
    path("myaccount/", user_views.myAccount, name="myaccount"),
    # orders
    path("start_order/", cart_views.start_order, name="start_order"),
    path("webhooks/stripe/", cart_views.stripe_webhook, name="stripe-webhooks"),
]
