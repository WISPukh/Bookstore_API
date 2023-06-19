from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from geopy.geocoders import Nominatim
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

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


class CartItemsViewSet(ModelViewSet):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartItemSerializer
    http_method_names = ['post', 'delete', 'get', 'patch', 'options']
    permission_classes = [IsAuthenticated]
    lookup_field = 'book_id'

    @swagger_auto_schema(
        responses={'200': openapi.Response(description='Cart List', schema=serializer_class)}
    )
    def list(self, request, *args, **kwargs):
        service = CartsService(self.request.user, self.model)
        returned_data = service.list()

        serialized_datas = CartSerializer(returned_data, many=False).data

        return Response(status=200, data=serialized_datas)

    def retrieve(self, request, *args, **kwargs):
        instance = self.model.objects.get_detailed_information(user_pk=request.user.pk, **kwargs)
        if not instance:
            return Response(status=404, data={'error': 'item not found'})
        return Response(self.serializer_class(instance).data)

    @swagger_auto_schema(
        request_body=AddToCardSerializer, responses={
            200: openapi.Response('Successfully added book to cart', schema=serializer_class),
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
        return Response(self.serializer_class(instance).data)

    @swagger_auto_schema(
        request_body=AmountForCartSerializer, responses={
            200: openapi.Response(description='Cart List', schema=serializer_class),
            400: openapi.Response(description='Book is not in cart or amount is not positive number')
        }
    )
    def partial_update(self, request, *args, **kwargs):
        amount = int(self.request.data.get('amount'))
        book = self.model.objects.filter(user_id=request.user.pk, status='CART', **kwargs).first()

        # TODO: make this a validation function
        if book is None:
            return Response(status=400, data={'error': f"Book with id: {kwargs.get('book_id')} doesn't exist in cart!"})

        if amount < 1:
            return Response(status=400, data={'error': 'amount should be a positive number!'})

        service = CartsService(user=self.request.user, model=self.model)
        instance = service.single_update(book, data=self.request.data)
        return Response(status=200, data=self.serializer_class(instance).data)

    @swagger_auto_schema(
        method='patch',
        request_body=RepresentationCartUpdateSerializer,
        responses={'200': openapi.Response(description='Cart List', schema=serializer_class)}
    )
    @action(methods=['patch'], detail=False, url_path='bulk')
    def bulk_patch(self, request, *args, **kwargs):
        items_ids_in_cart = self.model.objects.filter(
            user_id=request.user.pk, status='CART'
        ).values_list('book_id', flat=True)

        if not items_ids_in_cart:
            return Response(status=400, data={'error': 'Cart is empty!'})

        request_book_ids = set([item['book_id'] for item in request.data.get('cart')])

        unknown_ids = request_book_ids.difference(items_ids_in_cart)

        if unknown_ids:
            unknown_ids = list(map(str, unknown_ids))
            return Response(status=400, data={'error': f"Items with id: {', '.join(unknown_ids)} are not in cart!"})

        if any(item['amount'] < 1 for item in request.data.get('cart')):
            return Response(status=400, data={'error': "Amount of items should be a positive number!"})

        service = CartsService(self.request.user, self.model)
        datas = service.update_cart(data=self.request.data)
        return Response(status=200, data=self.serializer_class(datas, many=True).data)

    @swagger_auto_schema(responses={
        204: openapi.Response('Successfully deleted book from cart'),
        400: openapi.Response('Provided invalid book_id')
    })
    def destroy(self, request, *args, **kwargs):
        # for instance: kwargs={'book_id': '40'}
        book = self.model.objects.filter(user_id=request.user.pk, status='CART', **kwargs).first()
        if not book:
            return Response(status=400, data={'error': "You can't delete book that you don't have in cart!"})
        book.delete()
        return Response(status=204)
