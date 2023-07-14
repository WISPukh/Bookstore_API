from rest_framework import serializers

from author.models import Author
from bookstore.pagination.serializers import PaginationSerializer
from genres.models import Genre


class BookSerializer(serializers.Serializer):  # noqa
    id = serializers.IntegerField(read_only=True)
    in_stock = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False, default=200)
    genres = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all()),
        required=False
    )
    author = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(queryset=Author.objects.all()),
        required=False
    )
    release_date = serializers.DateField(required=False)
    writing_date = serializers.DateField(required=False)
    preview_image = serializers.ImageField(required=False, use_url=True)


class PaginationBookSerializer(PaginationSerializer):  # noqa
    result = serializers.ListSerializer(child=BookSerializer())


class ShortBookSerializer(serializers.Serializer):  # noqa
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()


class AddToCardSerializer(serializers.Serializer):  # noqa
    book_id = serializers.IntegerField()
    amount = serializers.IntegerField()
