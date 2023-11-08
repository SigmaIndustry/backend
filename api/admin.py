from django.contrib import admin

from .models import Review, Service, ServiceProvider

admin.site.register(Review)
admin.site.register(ServiceProvider)
admin.site.register(Service)
