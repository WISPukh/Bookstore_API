from rest_framework import serializers
from rest_framework.serializers import ListSerializer


class PrimitiveCartSerializer(serializers.Serializer):  # noqa
    book_id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)


class CartAddressSerializer(serializers.Serializer):  # noqa
    city = serializers.CharField(required=False)
    address = serializers.CharField(required=False)


class BaseCartSerializer(PrimitiveCartSerializer, CartAddressSerializer):  # noqa
    id = serializers.IntegerField(read_only=True)
    state = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    warranty_days = serializers.IntegerField(required=False)
    orders_id = serializers.CharField(read_only=True)
    orders_time = serializers.DateTimeField(read_only=True)


class CartItemSerializer(BaseCartSerializer):  # noqa
    total_orders_price = serializers.IntegerField(read_only=True, required=False)
    price_discounted = serializers.IntegerField(read_only=True, required=False)
    new_price = serializers.IntegerField(read_only=True, required=False)


class CartSerializer(serializers.Serializer):  # noqa
    total = serializers.IntegerField(read_only=False)
    persons_discounted_price = serializers.IntegerField(read_only=False)
    products = ListSerializer(child=CartItemSerializer())


class RepresentationCartUpdateSerializer(serializers.Serializer):  # noqa
    cart = serializers.ListSerializer(child=PrimitiveCartSerializer())
