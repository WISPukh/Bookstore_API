from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import UsersViewSet


router = SimpleRouter()
router.register(r'', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
