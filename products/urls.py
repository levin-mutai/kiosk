from rest_framework.routers import DefaultRouter
from views import ProductViewSet, OrderViewSet


router = DefaultRouter()

router.register(r"products", ProductViewSet, basename="Products_detail")
router.register(r"orders", OrderViewSet, basename="Orders_detail")

urlpatterns = router.urls
