from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:poll_id>/", views.entry, name="entry"),
    path("<int:poll_id>/results/", views.results, name="results"),
]
