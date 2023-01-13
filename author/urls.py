from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import AuthorViewSet

router = SimpleRouter()
router.register('', AuthorViewSet, basename='authors')

urlpatterns = [
    path('', include(router.urls))
]
