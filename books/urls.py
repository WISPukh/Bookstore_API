from rest_framework.routers import SimpleRouter

from .views import BookViewSet

router = SimpleRouter()
router.register(r'', BookViewSet, basename='book')

urlpatterns = router.urls
