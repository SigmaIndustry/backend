from django.urls import path

from .views import *

urlpatterns = [
    path("", index),
    path("service/list/@<provider_id>", service_of_provider),
    path("service/search", search_service),
    path("service/rate", rate_service),
    path("service/create", create_service),
    path("service/delete", delete_service),
    path("service/order", order_service),
    path("add_geolocation", add_geolocation),
    path("enum/sex", sex, name="Sex enums"),
    path("enum/roles", roles, name="Role enums"),
    path("enum/categories", categories, name="Category enums"),
    path("get_history/<str:email>", get_history),
]
