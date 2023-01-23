from rest_framework.serializers import ModelSerializer, ListSerializer

from bookstore.pagination.serializers import PaginationSerializer
from .models import Author


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class PaginationAuthorSerializer(PaginationSerializer):  # noqa
    result = ListSerializer(child=AuthorSerializer())
