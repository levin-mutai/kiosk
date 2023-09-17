from rest_framework.routers import DefaultRouter
from .views import ProductViews, OrderViewSet, OrderProductViewSet, CustomerViews


router = DefaultRouter(trailing_slash=False)

router.register(r"products", ProductViews, basename="Products_detail")
router.register(r"orders", OrderViewSet, basename="Orders_detail")
router.register(
    r"ordered_products", OrderProductViewSet, basename="Ordered_Products_detail"
)
router.register("customers", CustomerViews, basename="customer_detail")


urlpatterns = router.urls
