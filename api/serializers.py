from rest_framework import serializers

from .models import Geolocation, OrderHistoryEntry, Service, ServiceProvider


class ServiceSerializer(serializers.ModelSerializer):
    pictures = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = "__all__"

    @staticmethod
    def get_pictures(obj: Service):
        return obj.pictures.split(";")

    @staticmethod
    def get_rating(obj: Service):
        return obj.get_rating()

    @staticmethod
    def get_reviews(obj: Service):
        return None


class GeolocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocation
        fields = "__all__"


class ServiceProviderSerializer(serializers.ModelSerializer):
    geolocation = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProvider
        fields = [
            "business_name",
            "description",
            "phone_number",
            "city",
            "work_time",
            "geolocation",
            "created_at",
        ]

    @staticmethod
    def get_geolocation(obj: ServiceProvider):
        if not obj.geolocation:
            return None
        return GeolocationSerializer(obj.geolocation).data


class OrderHistoryEntrySerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()

    class Meta:
        model = OrderHistoryEntry
        fields = "__all__"

    @staticmethod
    def get_service(obj: OrderHistoryEntry):
        return ServiceSerializer(obj.service).data
