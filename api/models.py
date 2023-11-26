import statistics

from django.db import models

from __enums__ import CATEGORIES
from security.models import User


class Review(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    rating = models.FloatField(default=0.0)
    feedback = models.TextField(null=True, blank=True)


class Geolocation(models.Model):
    country = models.CharField(max_length=32)
    region = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    latitude = models.FloatField()
    longitude = models.FloatField()


class ServiceProvider(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=32)
    description = models.TextField()
    phone_number = models.CharField(max_length=9)  # +380[phone_number]
    city = models.CharField(max_length=32, null=True, blank=True)
    work_time = models.CharField(max_length=11)  # 09:00-15:00
    reviews = models.ManyToManyField(Review, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Service(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32)
    pictures = models.TextField()
    description = models.TextField()
    price = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORIES)
    provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, db_constraint=False
    )
    reviews = models.ManyToManyField(Review, blank=True)
    geolocation = models.ForeignKey(
        Geolocation, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_rating(self):
        return statistics.median(
            [review.rating for review in self.reviews.all()] or [0.0]
        )


class OrderHistoryEntry(models.Model):
    email = models.EmailField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
