from django.contrib import admin
from django.conf import settings
from django.http import JsonResponse
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("security/", include("security.urls")),
    path("", lambda req: JsonResponse({})),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
