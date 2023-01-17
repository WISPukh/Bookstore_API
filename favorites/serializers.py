from typing import Union

from rest_framework.serializers import ModelSerializer, IntegerField, Serializer, ListField

from books.models import Book
from books.serializers import BookSerializer
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


class SwaggerListRepresentation(Serializer):  # noqa
    favorite_item_id = IntegerField()
    book = BookSerializer(many=True)


class SwaggerPutRepresentation(Serializer):  # noqa
    book_ids = ListField(child=IntegerField())


class SwaggerCreateRepresentation(Serializer):  # noqa
    book_id = IntegerField()
