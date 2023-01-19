from rest_framework import routers

from .views import CartViewSet

router = routers.DefaultRouter()
router.register(r'', CartViewSet, basename='cart')

urlpatterns = router.urls
