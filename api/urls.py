from django.urls import path

from .views import *

urlpatterns = [
    path("", index),
    path("enum/sex", sex),
    path("enum/roles", roles),
    path("enum/categories", categories),
]
