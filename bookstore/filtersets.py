from functools import reduce
from typing import Optional

from django.db.models import CharField, Value, Q, QuerySet
from django.db.models.functions import Concat
from django_filters.rest_framework import CharFilter, NumberFilter
from django_filters.rest_framework import FilterSet

from author.models import Author
from books.models import Book
from genres.models import Genre


class BookFilterSet(FilterSet):
    author = CharFilter(method='filter_author')
    genre = CharFilter(method='filter_genre')
    price = NumberFilter()
    price__gt = NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Book
        fields = ['title', 'release_date', 'price', 'author', 'genre']

    @staticmethod
    def name_concatenate(first_part: str, second_part: str, value: str) -> Optional[QuerySet]:
        return Author.objects.all().annotate(
            author=Concat(
                first_part, Value(' '), second_part, output_field=CharField())
        ).filter(author__icontains=value).exclude('author')

    def filter_author(self, queryset, name, value):
        if value:
            authors = Author.objects.all().annotate(
                author=Concat(
                    'first_name', Value(' '), 'second_name', output_field=CharField())
            ).filter(author__icontains=value)
            if not authors.exists():
                return Book.objects.none()
            return reduce(lambda x, y: Q(x) | Q(y), list(queryset.filter(author__id=author.id) for author in authors))

    @staticmethod
    def filter_genre(queryset, name, value):
        if value:
            genres = Genre.objects.filter(title__icontains=value)
            return reduce(lambda x, y: Q(x) | Q(y), list(queryset.filter(genres__id=genre.id) for genre in genres))
