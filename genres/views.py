from rest_framework.viewsets import ModelViewSet

from bookstore.mixins import PaginationViewSetMixin
from .models import Genre
from .serializers import GenreSerializer, PaginationGenreSerializer


class GenreViewSet(PaginationViewSetMixin, ModelViewSet):
    serializer_class = GenreSerializer
    pagination_serializer_class = PaginationGenreSerializer
    model = Genre
    http_method_names = ['patch', 'get', 'post', 'delete']

    def get_queryset(self):
        return self.model.objects.all()
