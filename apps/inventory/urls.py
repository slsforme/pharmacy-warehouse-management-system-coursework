from rest_framework.routers import DefaultRouter
from .views import ArrivalViewSet, ArrivalItemViewSet, StockViewSet

router = DefaultRouter()
router.register("arrivals", ArrivalViewSet, basename="arrivals")
router.register("arrival-items", ArrivalItemViewSet, basename="arrival-items")
router.register("stock", StockViewSet, basename="stock")

urlpatterns = router.urls
