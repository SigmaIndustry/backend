from django.contrib import admin

from .models import Service, ServiceProvider

# admin.site.register(Review)
admin.site.register(ServiceProvider)
admin.site.register(Service)
