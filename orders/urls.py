from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet

order_router = DefaultRouter()
order_router.register('', OrderViewSet, basename='order')

urlpatterns = order_router.urls
