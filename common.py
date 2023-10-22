import json
from dataclasses import dataclass
from typing import Callable, Union

from django.core.handlers.wsgi import WSGIRequest
from django.urls import path
from rest_framework.response import Response

SEX = (
    ("M", "Male"),
    ("F", "Female"),
)

ROLES = (
    ("A", "Admin"),
    ("P", "Provider"),
    ("G", "Guest"),
)

CATEGORIES = (("00", "Food"),)


GET = ("GET",)
POST = ("POST",)


@dataclass
class InvalidData:
    fields: dict[str, Union[type, str]]

    def make_response(self):
        return Response(
            {
                "_description": "Provided fields are invalid.",
                "invalid_fields": {
                    k: v if type(v) is str else v.__name__
                    for k, v in self.fields.items()
                },
            },
            status=406,
        )


def get_data(
    request: WSGIRequest, require: dict[str, Union[type, str]]
) -> Union[dict, InvalidData]:
    print(request.body, request.POST)
    data = json.loads(request.body or request.POST)
    invalid: dict[str, Union[type, str]] = {}
    for field, field_type in require.items():
        if data.get(field) is None:
            invalid[field] = field_type
    if invalid:
        return InvalidData(invalid)
    return data


def filter_data(data: dict, *names: str):
    return {k: v for k, v in data.items() if k not in names}
