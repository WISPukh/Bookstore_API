from rest_framework.viewsets import ModelViewSet

from .models import Genre
from .serializers import GenreSerializer


class GenreViewSet(ModelViewSet):
    serializer_class = GenreSerializer
    model = Genre
    http_method_names = ['patch', 'get', 'post', 'delete']

    def get_queryset(self):
        return self.model.objects.all()
