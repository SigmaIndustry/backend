import json
from dataclasses import dataclass
from typing import Union

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.response import Response


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
    data = json.loads(request.body)
    invalid: dict[str, Union[type, str]] = {}
    for field, field_type in require.items():
        if data.get(field) is None and not str(field_type).startswith("?"):
            invalid[field] = field_type
    if invalid:
        return InvalidData(invalid)
    return data


def filter_data(data: dict, *names: str):
    return {k: v for k, v in data.items() if k not in names}
