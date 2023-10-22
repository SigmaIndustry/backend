from django.urls import path

from .views import *

urlpatterns = [
    path("register", register, name="Register user"),
    path("register_provider", register_provider, name="Register service provider"),
    path("login", login, name="Login user"),
    path("authenticate", authenticate, name="Authenticate user using token"),
]
