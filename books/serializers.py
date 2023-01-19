from rest_framework import serializers

from author.models import Author
from genres.models import Genre


class BookSerializer(serializers.Serializer):  # noqa
    id = serializers.IntegerField(read_only=True)
    in_stock = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False, default=200)
    genres = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all()))
    author = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Author.objects.all()))
    release_date = serializers.DateField(required=False)


class PaginationLinksBookSerializer(serializers.Serializer):  # noqa
    next = serializers.URLField(read_only=True)
    previous = serializers.URLField(read_only=True)


class PaginationBookSerializer(serializers.Serializer):  # noqa
    links = PaginationLinksBookSerializer()
    total_pages = serializers.IntegerField(read_only=True)
    page = serializers.IntegerField(read_only=True)
    page_size = serializers.IntegerField(read_only=True)
    result = serializers.ListSerializer(child=BookSerializer())
