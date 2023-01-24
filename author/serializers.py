from rest_framework.serializers import ModelSerializer, ListSerializer, Serializer, CharField

from books.serializers import ShortBookSerializer
from bookstore.pagination.serializers import PaginationSerializer
from .models import Author


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class PaginationAuthorSerializer(PaginationSerializer):  # noqa
    result = ListSerializer(child=AuthorSerializer())


class SuggestionList(Serializer):  # noqa
    first_name = CharField()
    second_name = CharField()
    book = ShortBookSerializer()

    def to_representation(self, instance):
        book = instance.book_set.first()
        author_data = {
            'first_name': instance.first_name,
            'second_name': instance.second_name,
        }
        book_data = None if not book else {'id': book.id, 'title': book.title}

        return author_data | {'book': book_data}
