import math
import re
from hashlib import sha512
from secrets import token_hex

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import ServiceProvider
from common import InvalidData, POST, filter_data, get_data
from .models import User
from .serializers import ServiceProviderSerializer, UserSerializer


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

    if User.objects.filter(email=data["email"]).first():
        return Response({"_description": "User already exists."}, status=409)

    if get_entropy(data["password"]) < 50:
        return Response({"_description": "Password is too weak."}, 400)

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

    email, password = data["token"].split(":")

    user = User.objects.filter(email=email, password=password).first()

    if not user:
        return Response({"_description": "Invalid token."}, status=404)

    provider = ServiceProvider.objects.filter(user=user).first()

    return Response(
        {
            "user": UserSerializer(user).data,
            "service_provider": ServiceProviderSerializer(provider).data
            if provider
            else None,
        },
        status=200,
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
