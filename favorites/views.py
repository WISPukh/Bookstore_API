from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from books.models import Book
from bookstore.mixins import PaginationViewSetMixin
from .models import Favorite
from .serializers import (
    FavoriteSerializer,
    FavoriteCreateSerializer, PaginationFavoriteSerializer,
)
from .swagger import SwaggerPutRepresentation, SwaggerCreateRepresentation


class FavoriteViewSet(PaginationViewSetMixin, GenericViewSet, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    serializer_class = FavoriteSerializer
    pagination_serializer_class = PaginationFavoriteSerializer
    model = Favorite
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().values('book_id')
        book_ids = list(element['book_id'] for element in queryset)
        queryset = self.paginate_queryset(list(self.model.objects.filter(book_id__in=book_ids)))
        self.pagination_class.serializer_class = self.pagination_serializer_class

        return self.get_paginated_response(queryset)

    @swagger_auto_schema(
        request_body=SwaggerPutRepresentation, responses={200: openapi.Response('', schema=FavoriteSerializer)}
    )
    @action(detail=False, methods=['put'])
    def change(self, request, *args, **kwargs):
        book_ids = self.request.data.get('book_ids')
        user = self.request.user

        self.model.objects.filter(user_id=user.id).delete()
        db_books = Book.objects.filter(pk__in=book_ids).order_by('id')
        self.model.objects.bulk_create(
            [self.model(user_id=user, book_id=book_id) for book_id in db_books]
        )

        return Response(FavoriteSerializer(list(self.model.objects.filter(book_id__in=book_ids)), many=True).data)

    @swagger_auto_schema(
        request_body=SwaggerCreateRepresentation, responses={200: openapi.Response('', schema=FavoriteSerializer)}
    )
    def create(self, request, *args, **kwargs):
        self.request.data.update(user_id=self.request.user.id)
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FavoriteCreateSerializer

        return self.serializer_class
