from rest_framework.routers import DefaultRouter
from .views import ProductViews,OrderViewSet


router = DefaultRouter(trailing_slash=False)

router.register(r"products", ProductViews, basename="Products_detail")
router.register(r"orders", OrderViewSet, basename="Orders_detail")

urlpatterns = router.urls
