# Generated by Django 4.2.7 on 2023-11-08 14:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_remove_service_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="price",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
