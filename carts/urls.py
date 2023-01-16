from django.urls import path, include
from rest_framework import routers

from .views import CartViewSet

router = routers.DefaultRouter()
router.register(r'', CartViewSet, basename='carts_cart')

urlpatterns = [
    path('', include(router.urls)),
]
