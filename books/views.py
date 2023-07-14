import os
from typing import Type, Optional

from django.core.files import File
from django.db import transaction
from django.db.models import Model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import parsers
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from author.models import Author
from bookstore.exceptions import BadRequestError
from bookstore.filtersets import BookFilterSet
from bookstore.mixins import PaginationViewSetMixin
from bookstore.utils import handle_user_exceptions
from genres.models import Genre
from .models import Book
from .serializers import BookSerializer, PaginationBookSerializer


class BookViewSet(PaginationViewSetMixin, ModelViewSet):
    model = Book
    queryset = model.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookFilterSet  # noqa
    parser_classes = (parsers.MultiPartParser,)
    pagination_serializer_class = PaginationBookSerializer
    OrderingFilter.ordering_description = (
        f'Takes field name: title or -title for example. '
        f'Applies to fields: {", ".join(serializer_class().get_fields())}'
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    @handle_user_exceptions
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # I use transaction.atomic() here to get around situation where instance data was correct and creation passed,
        # but m2m fields' values were not correct and raised BadRequestError.
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_to_create = serializer.data

        new_book = self.model.objects.create(**data_to_create)

        self.set_m2m_links(new_book, 'genres', Genre)
        self.set_m2m_links(new_book, 'author', Author)

        if image := request.data.get('preview_image'):
            new_book.preview_image.save(os.path.basename(str(image)), File(image), save=True)
        new_book.save()

        return Response(status=201, data=self.serializer_class(new_book).data)

    @handle_user_exceptions
    def update(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return Response(status=403, data='User has not any permissions')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        instance = self.get_object()

        field_model_mapping = {
            'genres': Genre,
            'author': Author
        }
        for field, model in field_model_mapping.items():
            if unknown_ids := self.set_m2m_links(instance, field, model):
                raise BadRequestError(
                    details=f"У модели {model.__name__} не существует таких id: {', '.join(unknown_ids)}"
                )

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return Response(self.serializer_class(instance).data)

    def set_m2m_links(self, instance: Book, field: str, model: Type[Model]) -> Optional[set]:
        if ids := self.request.data.get(field):
            ids = ids.split(',')
            if unknown_ids := self.check_existence('id', ids, model):
                return unknown_ids
            m2m_field = getattr(instance, field)
            m2m_field.set(ids, clear=True)

    @staticmethod
    def check_existence(field: str, values: list[str], model: Type[Model]) -> Optional[set]:
        """
        If given data is valid then we return empty set. If data with non-existent ids was passed, we return

        given ids that don't exist in database.
        """
        query = model.objects.filter(**{f'{field}__in': values})
        if len(values) == query.count():
            return set()

        database_ids = list(map(str, query.values_list('id', flat=True)))
        return set(values) - set(database_ids)
