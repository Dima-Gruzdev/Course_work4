from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings, views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("clients", include("development.urls", namespace="development")),
    path("users/", include("users.urls", namespace="users")),
    path("", views.home, name="home"),
    path("mailings/", include("mailings.urls", namespace="mailings")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
