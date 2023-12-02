# Generated by Django 4.2.7 on 2023-11-26 12:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_remove_geolocation_longitude"),
    ]

    operations = [
        migrations.AddField(
            model_name="geolocation",
            name="longitude",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]