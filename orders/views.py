from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from carts.models import Cart
from orders.errors import OrdersError
from orders.serializers import OrderOuterSerializer, OrderIdSerializer
from orders.services import OrderService


class OrderViewSet(GenericViewSet, ListModelMixin):
    serializer_class = OrderOuterSerializer
    model = Cart
    lookup_url_kwarg = 'orders_id'
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={'200': openapi.Response(description='Order list', schema=OrderOuterSerializer)})
    def list(self, request, *args, **kwargs):

        service = OrderService()
        data_to_serialize = service.list(user_pk=self.request.user.pk, model=self.model, *args, **kwargs)

        serializer = OrderOuterSerializer(data_to_serialize, many=True)

        return Response(status=200, data=serializer.data)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('order_id', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)]
    )
    @action(detail=False, methods=['get'], url_path="detail")
    def list_detail(self, request, *args, **kwargs):
        service = OrderService()
        order_id = self.request.query_params.get('order_id')
        if not order_id:
            return Response(status=404, data='Not Found')
        returned_data = service.list_detail(order_id, self.model, self.request.user.pk)
        serializer = OrderOuterSerializer(returned_data, many=False)
        return Response(status=200, data=serializer.data)

    @swagger_auto_schema(request_body=OrderIdSerializer)
    @action(detail=False, methods=['post'], url_path='pay')
    def pay(self, request, *args, **kwargs):
        service = OrderService()
        order_id = self.request.data.get('order_id')
        orders_owner = None
        order = Cart.objects.filter(order_id=order_id)

        if order.exists():
            orders_owner = order.first().user_id
        else:
            return Response(status=404, data='There is not order with this ID')

        if orders_owner != self.request.user.pk:
            return Response(status=404, data='Users order history doesnt contains order with this ID')
        try:
            service.pay(self.request.user.pk, order_id, self.model)
        except OrdersError as e:
            return Response(status=400, data={'message': f'{e}'})

        return Response(status=200, data="Order was successfully paid")
