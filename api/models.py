from django.db import models

from api.enums import CATEGORIES, SEX, ROLES


class User(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=GENDERS)
    profile_picture = models.CharField(max_length=512, null=True, blank=True)
    role = models.CharField(max_length=1, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    pass


class ServiceProvider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=32)
    description = models.TextField()
    phone_number = models.CharField(max_length=9)  # +380[phone_number]
    city = models.CharField(max_length=32, null=True, blank=True)
    work_time = models.CharField(max_length=11)  # 09:00-15:00
    reviews = models.ManyToManyField(Review)
    created_at = models.DateTimeField(auto_now_add=True)


class Service(models.Model):
    name = models.CharField(max_length=32)
    pictures = models.TextField()
    description = models.TextField()
    price = models.PositiveBigIntegerField(null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORIES)
    rating = models.BigIntegerField()
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    reviews = models.ManyToManyField(Review)
    created_at = models.DateTimeField(auto_now_add=True)
