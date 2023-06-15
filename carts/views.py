from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from geopy.geocoders import Nominatim
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from books.models import Book
from books.serializers import AddToCardSerializer
from carts.models import Cart
from carts.serializers import (
    CartSerializer, CartItemSerializer, BaseCartSerializer, RepresentationCartUpdateSerializer, AmountForCartSerializer
)
from .services import CartsService


class CartViewSet(GenericViewSet):
    model = Cart
    queryset = model.objects.all()
    serializer_class = BaseCartSerializer

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('zipcode', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)],
        responses={
            200: openapi.Response(description='check zipcode for validity')
        }
    )
    @action(methods=['get'], detail=False)
    def check_zipcode(self, request, *args, **kwargs):
        geolocator = Nominatim(user_agent="geoapiExercises")
        zipcode = self.request.query_params.get('zipcode')
        if not zipcode:
            return Response({'detail': "you should provide zipcode!"}, status=400)

        return Response({'is_valid': geolocator.geocode(zipcode).raw['display_name'].split()[-1] == 'Россия'})


class CartItemsViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet, UpdateModelMixin
):
    model = Cart
    queryset = model.objects.all()
    serializer_class = BaseCartSerializer
    http_method_names = ['post', 'delete', 'get', 'patch']
    permission_classes = [IsAuthenticated]
    lookup_field = 'book_id'

    @swagger_auto_schema(
        responses={'200': openapi.Response(description='Cart List', schema=CartSerializer)}
    )
    def list(self, request, *args, **kwargs):
        service = CartsService(self.request.user, self.model)
        returned_data = service.list()

        serialized_datas = CartSerializer(returned_data, many=False).data

        return Response(status=200, data=serialized_datas)

    @swagger_auto_schema(
        request_body=AddToCardSerializer, responses={
            200: openapi.Response('Successfully added book to cart', schema=CartItemSerializer),
            400: openapi.Response('Amount of books is a not positive number!'),
        }
    )
    def create(self, request, *args, **kwargs):
        book_id = self.request.data.get('book_id')
        book = Book.objects.filter(pk=book_id).first()

        if book is None:
            return Response(status=400, data={'error': f"Book with id: {book_id} doesn't exist!"})

        if self.request.data.get('amount') < 1:
            return Response(status=400, data={'error': 'amount should be a positive number!'})

        service = CartsService(user=self.request.user, model=Book)
        instance = service.add_to_cart(book=book, data=self.request.data)
        return Response(CartItemSerializer(instance).data)

    @swagger_auto_schema(
        request_body=AmountForCartSerializer,
        responses={'200': openapi.Response(description='Cart List', schema=CartItemSerializer)}
    )
    def partial_update(self, request, *args, **kwargs):
        amount = int(self.request.data.get('amount'))
        book = Book.objects.filter(pk=kwargs.get('book_id')).first()

        if book is None:
            return Response(status=400, data={'error': f"Book with id: {kwargs.get('book_id')} doesn't exist!"})

        if amount < 1:
            return Response(status=400, data={'error': 'amount should be a positive number!'})

        service = CartsService(user=self.request.user, model=Book)
        instance = service.single_update(book, data=self.request.data)
        return Response(status=200, data=self.serializer_class(instance).data)

    @swagger_auto_schema(
        method='patch',
        request_body=RepresentationCartUpdateSerializer,
        responses={'200': openapi.Response(description='Cart List', schema=CartItemSerializer)}
    )
    @action(methods=['patch'], detail=False, url_path='bulk')
    def patch(self, request, *args, **kwargs):
        items_in_cart = self.model.objects.filter(status='CART')

        if not items_in_cart:
            return Response(status=400, data={'error': 'Cart is empty!'})

        ids_not_in_cart = []
        for item in self.request.data.get('cart'):
            book_id = item.get('book_id')
            if not items_in_cart.filter(book_id=book_id).exists():
                ids_not_in_cart.append(str(book_id))

        if ids_not_in_cart:
            return Response(status=400, data={'error': f"Items with id: {', '.join(ids_not_in_cart)} are not in cart!"})

        service = CartsService(self.request.user, self.model)
        datas = service.update_cart(data=self.request.data, *args, **kwargs)
        return Response(status=200, data=CartItemSerializer(datas, many=True).data)

    @swagger_auto_schema(responses={
        204: openapi.Response('Successfully deleted book from cart'),
        400: openapi.Response('Provided invalid book_id')
    })
    def destroy(self, request, *args, **kwargs):
        # for instance: kwargs={'book_id': '40'}
        book = self.model.objects.filter(**kwargs).first()
        if not book:
            return Response(status=400, data={'error': "You can't delete book that you don't have in cart!"})
        book.delete()
        return Response(status=204)
