import random

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bookstore.pagination import BookstorePagination


class PaginationViewSetMixin:
    """
    ___________________________________
    Implements ModelViewSet list method
    ___________________________________
    """
    pagination_class = BookstorePagination
    pagination_serializer_class = None

    def list(self, request, *args, **kwargs):
        if not self.pagination_serializer_class:
            raise AttributeError(
                f'Attribute "pagination_serializer_class" must be included in {self.__class__.__name__}'
            )
        queryset = self.paginate_queryset(self.filter_queryset((self.get_queryset())))
        self.pagination_class.serializer_class = self.pagination_serializer_class
        return self.get_paginated_response(queryset)


class ItemsViewSetMixin(PaginationViewSetMixin, ModelViewSet):

    model = None

    def __init_subclass__(cls, **kwargs):
        if cls.model is None:
            raise NotImplemented

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter("amount", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)]
    )
    @action(methods=['get'], detail=False, url_path="recommendation")
    def list_recommendation(self, request, *args, **kwargs):
        # QuerySet does not support slices and this way implement the logic
        books = list(item['id'] for item in self.model.objects.all().values('id'))
        random.shuffle(books)
        items_amount = len(books)
        amount = int(request.query_params.get("amount"))
        data = self.model.objects.filter(id__in=books[:amount])

        if items_amount < amount:
            return Response(status=400, data={"Too large a number error": "Amount number out of items range"})
        serializer = self.serializer_class(instance=data, many=True)
        validated_data = serializer.data
        return Response(status=200, data=validated_data)
