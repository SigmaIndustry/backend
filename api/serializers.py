from rest_framework import serializers

from .models import Service, ServiceProvider


class ServiceSerializer(serializers.ModelSerializer):
    pictures = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "pictures",
            "description",
            "price",
            "category",
            "rating",
            "provider",
        ]

    @staticmethod
    def get_pictures(obj: Service):
        return obj.pictures.split(";")


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = [
            "business_name",
            "description",
            "phone_number",
            "city",
            "work_time",
            "created_at",
        ]
