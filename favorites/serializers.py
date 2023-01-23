from typing import Union

from rest_framework.serializers import ModelSerializer, IntegerField, ListSerializer

from books.models import Book
from books.serializers import BookSerializer
from bookstore.pagination.serializers import PaginationSerializer
from .models import Favorite


class FavoriteSerializer(ModelSerializer):
    favorite_item_id = IntegerField(source='id')
    book = BookSerializer(many=True)

    class Meta:
        model = Favorite
        fields = ('favorite_item_id', 'book')

    def to_representation(self, instance: Favorite) -> dict[str | Union[int | Book]]:
        return {
            'favorite_item_id': instance.id,
            'book': BookSerializer(Book.objects.get(pk=instance.book_id_id)).data
        }


class FavoriteCreateSerializer(FavoriteSerializer):
    class Meta:
        model = Favorite
        fields = ('user_id', 'book_id',)


class PaginationFavoriteSerializer(PaginationSerializer):  # noqa
    result = ListSerializer(child=FavoriteSerializer())
