import json
from dataclasses import dataclass
from typing import Callable

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
    fields: dict[str, type | str]

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
    request: WSGIRequest, require: dict[str, type | str]
) -> dict | InvalidData:
    data = json.loads(request.body)
    invalid: dict[str, type | str] = {}
    for field, field_type in require.items():
        if data.get(field) is None:
            invalid[field] = field_type
    if invalid:
        return InvalidData(invalid)
    return data
