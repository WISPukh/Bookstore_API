from rest_framework.routers import SimpleRouter

from .views import FavoriteViewSet

router = SimpleRouter()
router.register('', FavoriteViewSet, basename='favorite')

urlpatterns = router.urls
