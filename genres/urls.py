from rest_framework.routers import DefaultRouter

from genres.views import GenreViewSet

router = DefaultRouter()
router.register('', GenreViewSet, basename='genres')

urlpatterns = router.urls
