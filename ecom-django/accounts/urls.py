from django.urls import path
from django.contrib.auth.views import LogoutView

from accounts import views

app_name = "accounts"


urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("myaccount/", views.myAccount, name="myaccount"),
]