from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "core"

urlpatterns = [
    path("", views.landing_page, name="landing-page"),
]
