from django.urls import path

from .views import *

urlpatterns = [
    path("", index),
    path("service/search", search_service),
    path("service/rate", rate_service),
    path("service/create", create_service),
    path("service/order", order_service),
    path("enum/sex", sex, name="Sex enums"),
    path("enum/roles", roles, name="Role enums"),
    path("enum/categories", categories, name="Category enums"),
]
