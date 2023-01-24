from rest_framework.routers import SimpleRouter

from .views import AuthorViewSet, AuthorSuggestionViewSet

router = SimpleRouter()
router.register('', AuthorSuggestionViewSet, basename='suggestion')
router.register('', AuthorViewSet, basename='authors')
urlpatterns = router.urls
