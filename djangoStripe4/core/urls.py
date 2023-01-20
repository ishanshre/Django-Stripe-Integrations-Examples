from django.urls import path

from core import views
from cart import views as cart_views


app_name = "core"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/detail/', views.ProductDetailView.as_view(), name='detail'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),

    # urls for carts
    path('cart/add_to_cart/<int:pk>/', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/view/', cart_views.cart_view, name='cart_view'),
    path('cart/update/<int:pk>/<str:action>/', cart_views.cart_update, name='cart_update'),
]