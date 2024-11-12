from django.urls import path
from . import views


app_name = "website_v2"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("countries/", views.countries, name="countries"),
    # path("team/", views.team, name="team"),
    # path("gallery/", views.gallery, name="gallery"),
    path("career/", views.career, name="career"),
    path("contact/", views.contact, name="contact"),
]
