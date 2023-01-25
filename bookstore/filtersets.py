from functools import reduce

from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter, DateFilter

from author.models import Author
from books.models import Book
from genres.models import Genre


class BookFilterSet(FilterSet):
    author = CharFilter(method='filter_author')
    genre = CharFilter(method='filter_genre')
    price = NumberFilter()
    price_gte = NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = NumberFilter(field_name='price', lookup_expr='lte')
    release_date = DateFilter()
    release_date_lte = DateFilter(field_name='release_date', lookup_expr='lte')
    release_date_gte = DateFilter(field_name='release_date', lookup_expr='gte')
    writing_date = DateFilter()
    writing_date_lte = DateFilter(field_name='writing_date', lookup_expr='lte')
    writing_date_gte = DateFilter(field_name='writing_date', lookup_expr='gte')

    class Meta:
        model = Book
        fields = [
            'title', 'release_date', 'writing_date', 'price', 'author', 'genre'
        ]

    def filter_author(self, queryset, name, value):  # noqa
        if value:
            authors = Author.objects.all().annotate(
                author=Concat(
                    'first_name', Value(' '), 'second_name', output_field=CharField())
            ).filter(author__icontains=value)
            if not authors.exists():
                return Book.objects.none()
            return reduce(
                lambda x, y: x.union(y, all=False),
                list(queryset.filter(author__id=author.id) for author in authors)
            )

    @staticmethod
    def filter_genre(queryset, name, value):
        if value:
            genres = Genre.objects.filter(title__icontains=value)
            return reduce(
                lambda x, y: x.union(y, all=False),
                list(queryset.filter(genres__id=genre.id) for genre in genres)
            )
