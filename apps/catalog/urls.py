from rest_framework.routers import DefaultRouter
from .views import DrugGroupViewSet, DrugViewSet, ManufacturerViewSet, SupplierViewSet

router = DefaultRouter()
router.register("drug-groups", DrugGroupViewSet, basename="drug-groups")
router.register("manufacturers", ManufacturerViewSet, basename="manufacturers")
router.register("suppliers", SupplierViewSet, basename="suppliers")
router.register("drugs", DrugViewSet, basename="drugs")

urlpatterns = router.urls
