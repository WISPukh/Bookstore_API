from rest_framework import routers

from .views import CartViewSet, CartItemsViewSet

cart_router = routers.SimpleRouter()
cart_router.register(r'', CartViewSet, basename='cart')

cart_items_router = routers.SimpleRouter()
cart_items_router.register('items', CartItemsViewSet, basename='cart_items')

urlpatterns = cart_router.urls + cart_items_router.urls
