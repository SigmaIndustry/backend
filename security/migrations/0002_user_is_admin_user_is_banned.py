# Generated by Django 4.2.7 on 2023-11-24 20:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("security", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_admin",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="is_banned",
            field=models.BooleanField(default=False),
        ),
    ]
