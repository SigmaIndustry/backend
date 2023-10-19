from django.urls import path
from .views import *


def make_urls(cls):
    return [
        path(f"{cls.__name__.lower()}/{method}", fn)
        for method, fn in cls.__dict__.items()
        if not method.startswith("_")
    ]


urlpatterns = [
    path("", index),
    *make_urls(List),
    *make_urls(Auth),
]
