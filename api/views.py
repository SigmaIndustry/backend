from typing import Callable

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Service
from common import CATEGORIES, GET, InvalidData, POST, ROLES, SEX, get_data
from .serializers import ServiceSerializer


def iterate_enum(enum):
    return {item[0]: item[1] for item in enum}


@api_view(("GET",))
def index(request):
    return Response({"1": True})


@api_view(GET)
def sex(request: WSGIRequest):
    return Response(iterate_enum(SEX))


@api_view(GET)
def roles(request: WSGIRequest):
    return Response(iterate_enum(ROLES))


@api_view(GET)
def categories(request: WSGIRequest):
    return Response(iterate_enum(CATEGORIES))


class ServiceMatches:
    def __init__(self):
        self._list: set[Service] = set()

    @property
    def list(self):
        return list(self._list)

    def add(self, service: Service):
        self._list.add(service)
        return self

    def filter(self, predicate: Callable):
        removed = set()
        for item in self._list:
            if not predicate(item):
                removed.add(item)
        self._list = {item for item in self._list if item not in removed}
        return self


@api_view(POST)
def search_service(request: WSGIRequest):
    data = get_data(
        request,
        require={
            "query": str,
            "page_limit": "?int",
            "page_offset": "?int",
            "min_price": "?int",
            "max_price": "?int",
            "category": "?str",
            "min_rating": "?int",
            "has_reviews": "?bool",
        },
    )

    if type(data) is InvalidData:
        return data.make_response()

    query = data["query"].lower()
    matches = ServiceMatches()

    # Find using the query
    for service in Service.objects.all():
        if query in service.name.lower():
            matches.add(service)

    # Filter
    if data.get("min_price"):
        matches.filter(lambda service: service.price >= float(data.get("min_price")))
    if data.get("max_price"):
        matches.filter(lambda service: service.price <= float(data.get("max_price")))

    if data.get("category"):
        matches.filter(lambda service: service.category == data.get("category"))

    if data.get("min_rating"):
        matches.filter(lambda service: service.rating >= data.get("min_rating"))

    if data.get("has_reviews"):
        matches.filter(
            lambda service: bool(len(service.reviews.all()) != 0)
            == bool(data.get("has_reviews"))
        )
    page_limit = int(data.get("page_limit", 1))
    page_offset = int(data.get("page_offset", 0))

    return Response(
        {
            "size": len(matches.list),
            "results": [
                ServiceSerializer(service).data
                for service in matches.list[page_offset:page_offset+page_limit]
            ],
        }
    )
