import json
from hashlib import sha512
from secrets import token_hex
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.enums import CATEGORIES, SEX, ROLES
from api.models import User


@api_view(("GET",))
def index(request):
    return Response({"1": True})


class List:
    @staticmethod
    def _iterate(enum):
        return {item[0]: item[1] for item in enum}

    @staticmethod
    @api_view(("GET",))
    def sex(request: WSGIRequest):
        return Response(List._iterate(SEX))

    @staticmethod
    @api_view(("GET",))
    def roles(request: WSGIRequest):
        return Response(List._iterate(ROLES))

    @staticmethod
    @api_view(("GET",))
    def categories(request: WSGIRequest):
        return Response(List._iterate(CATEGORIES))


class Auth:
    @staticmethod
    def _gen_password(password: str):
        salt = token_hex(2)
        return salt, sha512(f"{salt}{password}".encode()).hexdigest()

    @staticmethod
    @api_view(("POST",))
    def register(request: WSGIRequest):
        data = json.loads(request.body)
        salt, password = Auth._gen_password(data.get("password"))
        user = User(
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            password=password,
            salt=salt,
            birth_date=data.get("birth_date"),
            sex=data.get("sex"),
            profile_picture=data.get("profile_picture"),
            role=data.get("role"),
        )
        # user.save()
        return Response({"token": f"{user.email}:{user.password}"})

    @staticmethod
    @api_view(("POST",))
    def login(request: WSGIRequest):
        data = json.loads(request.body)

        user = User.objects.filter(
            email=data.get("email"), password=data.get("password")
        ).first()
        if user is None:
            return Response({"error": "Користувач не знайден"})

        return Response({"token": f"{user.email}:{user.password}"})
