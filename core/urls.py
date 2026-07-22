from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "core"

urlpatterns = [
    path("", views.landing_page, name="landing-page"),
    path("services/", views.services_page, name="services"),
    path("services/spine-care/", views.service_detail, {"slug": "spine-care"}, name="service-spine"),
    path("services/sports-rehab/", views.service_detail, {"slug": "sports-rehab"}, name="service-sports"),
    path("services/geriatric-care/", views.service_detail, {"slug": "geriatric-care"}, name="service-geriatric"),
    path("services/pain-solutions/", views.service_detail, {"slug": "pain-solutions"}, name="service-pain"),
    path("services/neuro-care/", views.service_detail, {"slug": "neuro-care"}, name="service-neuro"),
    path("about/", views.about_page, name="about"),
    path("team/", views.team_page, name="team"),
    path("contact/", views.contact_page, name="contact"),
]
