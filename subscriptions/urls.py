from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("checkout", views.checkout, name="checkout"),
    path("success", views.success, name="success"),
    path("cancel", views.cancel, name="cancel"),
]
