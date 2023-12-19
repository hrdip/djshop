from .. views.admin import CategoryAdminViewSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("categories", CategoryAdminViewSet, basename="categories")

urlpatterns = [] + router.urls 