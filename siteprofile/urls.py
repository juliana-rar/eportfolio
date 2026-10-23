from django.urls import path

from . import views

app_name = "siteprofile"

urlpatterns = [
    path("about/", views.about, name="about"),
]
