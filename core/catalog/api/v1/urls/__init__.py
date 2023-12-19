from django.urls import path, include

urlpatterns = [
    path("front/", include("catalog.api.v1.urls.front")),
    path("admin/", include("catalog.api.v1.urls.admin")),
]
