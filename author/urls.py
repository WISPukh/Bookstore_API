from rest_framework.routers import SimpleRouter

from .views import AuthorViewSet

router = SimpleRouter()
router.register('', AuthorViewSet, basename='author')

urlpatterns = router.urls
