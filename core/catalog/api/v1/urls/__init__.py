from django.urls import path, include

urlpatterns = [
    path("", include("catalog.api.v1.urls.front")),
    path("admin/", include("catalog.api.v1.urls.admin")),
]
