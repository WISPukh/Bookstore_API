from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet

order_router = DefaultRouter()
order_router.register('', OrderViewSet, basename='orders')

urlpatterns = order_router.urls
