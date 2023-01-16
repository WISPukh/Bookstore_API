from django.db import transaction
from django.db.transaction import atomic
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from carts.models import Cart
from carts.serializers import CartSerializer, CartItemSerializer
from books.models import Book
from .errors import UnexpectedItemError
from .services import CartsService

from orders.tasks import order_created


class BaseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return self.model.objects.all()


class CartViewSet(BaseViewSet):
    serializer_class = CartSerializer
    model = Cart
    http_method_names = ['patch', 'get', 'post', 'delete']
    permission_classes = [IsAuthenticated]

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

    def list(self, request, *args, **kwargs):
        service = CartsService(self.request.user, self.model)
        returned_data = service.list()

        serialized_datas = self.serializer_class(returned_data, many=False).data

        return Response(status=200, data=serialized_datas)

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
        # TODO: Fix Celery
        # else:
        #     order_created.delay(
        #         order_id=returned_data['products'][0]['order_id']
        #     )

        serialized_datas = self.serializer_class(returned_data, many=False)

        return Response(status=200, data=serialized_datas.data)