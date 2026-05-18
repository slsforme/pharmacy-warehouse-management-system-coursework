from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserViewSet

router = DefaultRouter()
router.register("roles", RoleViewSet, basename="roles")
router.register("", UserViewSet, basename="users")

urlpatterns = router.urls
