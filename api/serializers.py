from rest_framework import serializers

from .models import Service, ServiceProvider


class ServiceSerializer(serializers.ModelSerializer):
    pictures = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = "__all__"

    @staticmethod
    def get_pictures(obj: Service):
        return obj.pictures.split(";")

    @staticmethod
    def get_rating(obj: Service):
        return obj.get_rating()


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
