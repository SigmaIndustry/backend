from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common import CATEGORIES, GET, ROLES, SEX


@api_view(("GET",))
def index(request):
    return Response({"1": True})


def iterate_enum(enum):
    return {item[0]: item[1] for item in enum}


@api_view(GET)
def sex(request: WSGIRequest):
    return Response(iterate_enum(SEX))


@api_view(GET)
def roles(request: WSGIRequest):
    return Response(iterate_enum(ROLES))


@api_view(GET)
def categories(request: WSGIRequest):
    return Response(iterate_enum(CATEGORIES))
