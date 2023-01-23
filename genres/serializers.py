from rest_framework.serializers import ModelSerializer, ListSerializer

from bookstore.pagination.serializers import PaginationSerializer
from genres.models import Genre


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PaginationGenreSerializer(PaginationSerializer):  # noqa
    result = ListSerializer(child=GenreSerializer())
