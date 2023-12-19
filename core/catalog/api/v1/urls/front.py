from django.urls import path, include
from .. views.front import CategoryFrontViewSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("category", CategoryFrontViewSet, basename="category")

urlpatterns = [] + router.urls 
