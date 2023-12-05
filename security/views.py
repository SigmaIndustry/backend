import math
import re
from hashlib import sha512
from secrets import token_hex

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from __enums__ import EMAIL_PATTERN, POST
from __utils__ import InvalidData, authenticate_token, filter_data, get_data
from api.models import ServiceProvider
from api.serializers import ServiceProviderSerializer

from .models import User
from .serializers import UserSerializer


class UserApiView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def get_entropy(password: str):
    return math.log2(len(set(password)) ** len(password))


def encrypt_password(salt: str, password: str):
    return sha512(f"{salt}{password}".encode()).hexdigest()


def encrypt_unsalted_password(password: str):
    salt = token_hex(2)
    return salt, encrypt_password(salt, password)


@api_view(POST)
def register(request: WSGIRequest):
    data = get_data(
        request,
        require={
            "email": str,
            "password": str,
            "first_name": str,
            "last_name": str,
            "birth_date": "YYYY-MM-DD",
            "sex": str,
            "profile_picture": str,
            "role": str,
        },
    )

    if type(data) is InvalidData:
        return data.make_response()

    if not re.fullmatch(EMAIL_PATTERN, data["email"]):
        return Response({"_description": "Email is invalid.", "field": "email"}, 400)

    if User.objects.filter(email=data["email"]).first():
        return Response({"_description": "User already exists."}, status=409)

    if get_entropy(data["password"]) < 50:
        return Response(
            {"_description": "Password is too weak.", "field": "password"}, 400
        )

    user = User(**data)
    user.salt, user.password = encrypt_unsalted_password(data["password"])
    user.role = "M" if data["role"] not in ["G", "P"] else data["role"]
    user.save()

    return Response({"token": user.get_token()}, status=200)


@api_view(POST)
def login(request: WSGIRequest):
    data = get_data(
        request,
        require={
            "email": str,
            "password": str,
        },
    )

    if type(data) is InvalidData:
        return data.make_response()

    user = User.objects.filter(email=data["email"]).first()

    if not user or user.password != encrypt_password(user.salt, data["password"]):
        return Response({"_description": "Email or password are invalid."}, status=404)

    return Response({"token": user.get_token()}, status=200)


@api_view(POST)
def authenticate(request: WSGIRequest):
    data = get_data(
        request,
        require={
            "token": str,
        },
    )

    if type(data) is InvalidData:
        return data.make_response()

    user, provider = authenticate_token(data["token"])

    if not user:
        return Response({"_description": "Invalid token."}, status=404)

    if user.is_banned:
        return Response({"_description": "You are banned."}, status=403)

    return Response(
        {
            "user": UserSerializer(user).data,
            "service_provider": ServiceProviderSerializer(provider).data
            if provider
            else None,
        }
    )


@api_view(POST)
def register_provider(request: WSGIRequest):
    data = get_data(
        request,
        require={
            "email": str,
            "business_name": str,
            "description": str,
            "phone_number": str,
            "city": str,
            "work_time": str,
        },
    )

    if type(data) is InvalidData:
        return data.make_response()

    user = User.objects.filter(email=data["email"]).first()
    if not user:
        return Response(
            {"_description": f"User {data['email']} not found."}, status=404
        )

    provider = ServiceProvider(
        **filter_data(data, "email", "phone_number"),
        user=user,
        phone_number=re.sub(r"^(\+38)?0", "", data["phone_number"]),
    )
    provider.save()

    return Response({"token": user.get_token()}, status=200)


@api_view(POST)
def update(request: WSGIRequest):
    data = get_data(
        request,
        require={
            "token": str,
            "email": "?str",
            "password": "?str",
            "first_name": "?str",
            "last_name": "?str",
            "birth_date": "?YYYY-MM-DD",
            "sex": "?str",
            "profile_picture": "?str",
            "role": "?str",
            # Provider:
            "business_name": "?str",
            "description": "?str",
            "phone_number": "?str",
            "city": "?str",
            "work_time": "?str",
        },
    )

    if type(data) is InvalidData:
        return data.make_response()

    user, provider = authenticate_token(data["token"])

    if not user:
        return Response({"_description": "Invalid token."}, status=404)

    if provider:
        for key, value in filter_data(
            data,
            "token",
            "email",
            "password",
            "first_name",
            "last_name",
            "birth_date",
            "sex",
            "profile_picture",
            "role",
        ).items():
            setattr(provider, key, value)
        provider.save()

    for key, value in filter_data(
        data, "business_name", "description", "phone_number", "city", "work_time"
    ).items():
        setattr(user, key, value)

    if data.get("password"):
        user.salt, user.password = encrypt_unsalted_password(data["password"])
    user.save()

    return Response(
        {
            "user": UserSerializer(user).data,
            "service_provider": ServiceProviderSerializer(provider).data
            if provider
            else None,
        }
    )


@api_view(POST)
def get_provider(request: WSGIRequest):
    data = get_data(
        request,
        require={
            "provider_id": int,
        },
    )

    if type(data) is InvalidData:
        return data.make_response()

    provider = ServiceProvider.objects.filter(id=data["provider_id"]).first()

    if not provider:
        return Response({"_description": "Provider not found."}, status=404)

    return Response(ServiceProviderSerializer(provider).data)


@api_view(POST)
def ban(request: WSGIRequest):
    data = get_data(
        request,
        require={
            "token": str,
            "email": str,
            "reason": "?str",
        },
    )

    if type(data) is InvalidData:
        return data.make_response()

    request_user, _ = authenticate_token(data["token"])
    if not request_user.is_admin:
        return Response({"_description": "No permission."}, status=403)

    user = User.objects.filter(email=data["email"]).first()
    if not user:
        return Response(
            {"_description": "User not found.", "field": "token"}, status=404
        )

    user.is_banned = True
    user.save()

    return Response({})
