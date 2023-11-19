import threading
from typing import Callable

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from __enums__ import CATEGORIES, GET, POST, ROLES, SEX
from __utils__ import (
    InvalidData,
    authenticate_token,
    filter_data,
    get_data,
)
from .models import Review, Service, ServiceProvider
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
                for service in matches.list[page_offset : page_offset + page_limit]
            ],
        }
    )


@api_view(POST)
def rate_service(request: WSGIRequest):
    data = get_data(
        request,
        require={
            "token": str,
            "service_id": int,
            "rating": "float >=0 <=5",
            "feedback": "?str",
        },
    )

    if type(data) is InvalidData:
        return data.make_response()

    service = Service.objects.filter(id=int(data["service_id"])).first()
    if not service:
        return Response(
            {"_description": "Service not found.", "field": "service_id"}, status=404
        )

    user, _ = authenticate_token(data["token"])

    if not user:
        return Response(
            {"_description": "User not found.", "field": "token"}, status=404
        )

    rating = Review(
        user=user,
        rating=max(min(data["rating"], 5.0), 0.0),
        feedback=data.get("feedback") or None,
    )
    rating.save()
    service.reviews.add(rating)

    return Response({"rating_id": rating.id})


@api_view(POST)
def create_service(request: WSGIRequest):
    data = get_data(
        request,
        require={
            "provider_id": int,
            "name": str,
            "pictures": "list[str]",
            "description": "?str",
            "price": float,
            "category": str,
        },
    )

    if type(data) is InvalidData:
        return data.make_response()

    provider = ServiceProvider.objects.filter(id=data["provider_id"]).first()

    if not provider:
        return Response({"_description": "Provider not found."}, status=404)

    service = Service(
        provider=data["provider_id"],
        pictures=";".join(data["pictures"]),
        **filter_data(data, "provider_id", "pictures"),
    )
    service.save()

    return Response(ServiceSerializer(service).data)


@api_view(POST)
def order_service(request: WSGIRequest):
    data = get_data(
        request,
        require={"token": str, "service_id": "str", "message": "str"},
    )

    if type(data) is InvalidData:
        return data.make_response()

    user, _ = authenticate_token(data["token"])

    if not user:
        return Response(
            {"_description": "User not found.", "field": "token"}, status=404
        )

    service = Service.objects.filter(id=data["service_id"]).first()

    if not service:
        return Response(
            {"_description": "Service not found.", "field": "service"}, status=404
        )

    msg = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-size: 1.25rem;">
    <table style="border: none; width: fit-content; margin: 0 auto; border-collapse: collapse;">
        <tr>
            <td style="padding: 1rem 0;">You have a new order from {user.first_name} {user.last_name} on your service
            <a href="{request.build_absolute_uri("/service/" + str(service.id))}">{service.name}</a>.</td>
        </tr>
        <tr><td style="padding: 1rem 0;"><h3 style="margin: 0;">They left the following message:</h3></td></tr>
        <tr><td style="padding: 1rem 0;"><q style="border-left: 4px solid black; padding: 1rem;">{data["message"]}</q></td></tr>
        <tr style="font-size: 0.75rem;"><td style="padding: 1rem 0;">SigmaIndustry © 2023</td></tr>
    </table>
    </body>
    </html>
    """
    mail = EmailMessage(
        f"New order of {service.name}", msg, settings.EMAIL_HOST_USER, [user.email]
    )
    mail.content_subtype = "html"
    mail.send()

    return Response({})
