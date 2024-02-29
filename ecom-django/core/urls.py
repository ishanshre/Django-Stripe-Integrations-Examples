from django.urls import path


from core import views


app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/detail/", views.ProductDetailView.as_view(), name="detail"),
    path("success/", views.SuccessView.as_view(), name="success"),
    path("cancel/", views.CancelView.as_view(), name="cancel"),
]
