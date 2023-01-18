from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Book
from .serializers import BookSerializer
from bookstore.filtersets import BookFilterSet


class BookViewSet(viewsets.ModelViewSet):
    model = Book
    queryset = model.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilterSet
    pagination_class = PageNumberPagination

    ordering_fields = ['title']

    http_method_names = ['get', 'post', 'patch', 'delete']


    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_to_create = serializer.data
        genres_ids = data_to_create.pop("genres") if "genres" in data_to_create else None
        authors_ids = data_to_create.pop("author") if "author" in data_to_create else None
        new_book = self.model.objects.create(**data_to_create)
        new_book.genres.set(genres_ids)
        new_book.author.set(authors_ids)
        new_book.save()

        return Response(status=201, data=serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter()
        serialized_items = self.serializer_class(list(queryset), many=True)
        return Response(status=200, data=serialized_items.data)

    def update(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return Response(status=403, data='User has not any permissions')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        instance = self.get_object()

        genres_ids = validated_data.pop("genres") if "genres" in validated_data else None
        author_ids = validated_data.pop("author") if "author" in validated_data else None
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if author_ids:
            instance.author.set(author_ids)
        if genres_ids:
            instance.genres.set(genres_ids)
        instance.save()

        return Response(self.serializer_class(instance).data)
