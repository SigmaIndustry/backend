from django.db import models

from __enums__ import ROLES, SEX


class User(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    salt = models.CharField(max_length=4)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX)
    profile_picture = models.CharField(max_length=512, null=True, blank=True)
    role = models.CharField(max_length=1, choices=ROLES)
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_token(self):
        return f"{self.email}:{self.password}"
