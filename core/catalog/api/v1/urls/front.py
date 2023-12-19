from django.urls import path, include
from .. import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("category", views.CategoryViewSet, basename="category")

urlpatterns = []+router.urls 
