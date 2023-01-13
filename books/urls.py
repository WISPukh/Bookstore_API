from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import BookViewSet

router = SimpleRouter()
router.register(r'', BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
]
