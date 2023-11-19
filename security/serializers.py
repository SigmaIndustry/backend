from rest_framework import serializers

from __enums__ import ROLES, SEX
from .models import User


class UserSerializer(serializers.ModelSerializer):
    sex = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

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

    @staticmethod
    def get_sex(obj: User):
        for key, value in SEX:
            if key == obj.sex:
                return value
        return "Unknown"

    @staticmethod
    def get_role(obj: User):
        for key, value in ROLES:
            if key == obj.role:
                return value
        return "Unknown"
