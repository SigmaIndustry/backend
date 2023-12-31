# Generated by Django 4.2.7 on 2023-11-26 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_geolocation_longitude"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="serviceprovider",
            name="geolocation",
        ),
        migrations.AddField(
            model_name="service",
            name="geolocation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.geolocation",
            ),
        ),
    ]
