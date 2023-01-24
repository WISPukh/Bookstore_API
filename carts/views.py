from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from geopy.geocoders import Nominatim
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
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
        zipcode = self.request.data.get('zipcode')
        geolocator = Nominatim(user_agent="geoapiExercises")
        if not zipcode:
            return Response({'detail': "You should enter zipcode"}, status=400)

        data_region = geolocator.geocode(zipcode)

        if not data_region:
            return Response({'detail': "Zipcode is invalid!"}, status=400)

        if not data_region.raw['display_name'].split()[-1] == 'Россия':
            return Response({'detail': "Zipcode must be from Russia!"}, status=400)

        service = CartsService(self.request.user, self.model)
        try:
            returned_data = service.make_order(
                self.request.data, self.model
            )
        except UnexpectedItemError as e:
            return Response(status=400, data=e)

        serialized_datas = OrderOuterSerializer(returned_data, many=False)

        return Response(status=200, data=serialized_datas.data)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('zipcode', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)],
        responses={
            200: openapi.Response(description='check zipcode for validity')
        }
    )
    @action(methods=['get'], detail=False, permission_classes=[AllowAny])
    def check_zipcode(self, request, *args, **kwargs):
        geolocator = Nominatim(user_agent="geoapiExercises")
        zipcode = self.request.query_params.get('zipcode')
        if not zipcode:
            return Response({'detail': "you should provide zipcode!"}, status=400)

        return Response({'is_valid': geolocator.geocode(zipcode).raw['display_name'].split()[-1] == 'Россия'})
