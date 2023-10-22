from django.urls import path

from .views import *

urlpatterns = [
    path("", index),
    path("enum/sex", sex, name="Sex enums"),
    path("enum/roles", roles, name="Role enums"),
    path("enum/categories", categories, name="Category enums"),
]
