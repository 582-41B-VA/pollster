from django.contrib import admin
from django.urls import include, path

import polls.views

urlpatterns = [
    path("", polls.views.index, name="home"),
    path("polls/", include("polls.urls")),
    path("subscriptions/", include("subscriptions.urls")),
    path("admin/", admin.site.urls),
]
