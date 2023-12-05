from django.urls import path
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r"users", UserApiView)


urlpatterns = [
    path("register", register, name="Register user"),
    path("register_provider", register_provider, name="Register service provider"),
    path("login", login, name="Login user"),
    path("authenticate", authenticate, name="Authenticate user using token"),
    path("update", update),
    path("get_provider", get_provider),
    path("ban", ban),
] + router.urls
