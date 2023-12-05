from rest_framework import serializers

from .models import Geolocation, OrderHistoryEntry, Service, ServiceProvider


class GeolocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocation
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    pictures = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    geolocation = serializers.SerializerMethodField()

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

    @staticmethod
    def get_geolocation(obj: Service):
        if not obj.geolocation:
            return None
        return GeolocationSerializer(obj.geolocation).data


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = [
            "id",
            "business_name",
            "description",
            "phone_number",
            "city",
            "work_time",
            "created_at",
        ]


class OrderHistoryEntrySerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()

    class Meta:
        model = OrderHistoryEntry
        fields = "__all__"

    @staticmethod
    def get_service(obj: OrderHistoryEntry):
        return ServiceSerializer(obj.service).data
