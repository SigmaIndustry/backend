from rest_framework import serializers

from api.models import ServiceProvider
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "sex",
            "profile_picture",
            "role",
            "created_at",
        ]
