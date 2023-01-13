from django.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework.urls import path

from genres.views import GenreViewSet

router = DefaultRouter()
router.register('', GenreViewSet, basename='genres_genre')

urlpatterns = [
    path('', include(router.urls)),
]
