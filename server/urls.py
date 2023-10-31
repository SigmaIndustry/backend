from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("security/", include("security.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
