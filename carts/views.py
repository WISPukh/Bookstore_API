from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from books.models import Book
from carts.models import Cart
from carts.serializers import (
    CartSerializer, CartItemSerializer, BaseCartSerializer, RepresentationCartUpdateSerializer, CartAddressSerializer
)
from orders.serializers import OrderOuterSerializer
from .errors import UnexpectedItemError
from .services import CartsService


class CartViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = BaseCartSerializer
    model = Cart
    http_method_names = ['patch', 'get', 'post']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.all()

    @swagger_auto_schema(
        request_body=RepresentationCartUpdateSerializer,
        responses={'200': openapi.Response(description='Cart List', schema=CartItemSerializer)}
    )
    @action(detail=False, methods=['patch'], url_path='update_cart')
    def update_cart(self, request, *args, **kwargs):
        items = Book.objects.all()
        if not all(
                [items.filter(id=item['book_id']).exists() for item in self.request.data.get("cart")]
        ):
            return Response(status=400, data="There is not item with this id")

        service = CartsService(self.request.user, self.model)
        datas = service.update_cart(data=self.request.data, *args, **kwargs)
        return Response(status=200, data=CartItemSerializer(datas, many=True).data)

    @swagger_auto_schema(
        responses={'200': openapi.Response(description='Cart List', schema=CartSerializer)}
    )
    def list(self, request, *args, **kwargs):
        service = CartsService(self.request.user, self.model)
        returned_data = service.list()

        serialized_datas = CartSerializer(returned_data, many=False).data

        return Response(status=200, data=serialized_datas)

    @swagger_auto_schema(
        request_body=CartAddressSerializer,
        responses={'200': openapi.Response(description='Made order detail', schema=OrderOuterSerializer)}
    )
    @action(detail=False, methods=['post'], url_path='make_order')
    @transaction.atomic()
    def make_order(self, request, *args, **kwargs):
        service = CartsService(self.request.user, self.model)
        try:
            returned_data = service.make_order(
                self.request.data, self.model
            )
        except UnexpectedItemError as e:
            return Response(status=400, data=e)

        serialized_datas = OrderOuterSerializer(returned_data, many=False)

        return Response(status=200, data=serialized_datas.data)
