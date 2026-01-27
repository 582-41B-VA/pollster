from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:poll_id>/", views.entry, name="entry"),
    path("<int:poll_id>/submit/", views.entry_submit, name="entry_submit"),
    path("<int:poll_id>/results/", views.results, name="results"),
    path("create/", views.create_poll, name="create_poll"),
    path("create/submit/", views.create_poll_submit, name="create_poll_submit"),
]
