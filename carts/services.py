import uuid
from datetime import datetime

from books.models import Book
from carts.errors import UnexpectedItemError
from carts.models import Cart
from carts.serializers import CartItemSerializer


class CartsService:

    def __init__(self, user, model, *args, **kwargs):
        self.user = user
        self.model = model
        super().__init__(*args, **kwargs)

    def list(self):
        queryset = self.model.objects.filter(user_id=self.user.pk, status='CART').order_by('id').values()
        returned_data = self.model.objects.get_total_products_information(self.user.pk, ['CART'])

        for index, product in enumerate(returned_data['products']):
            product.update(queryset[index])

        return returned_data

    def make_order(self, data, model):
        items_to_update = Cart.objects.filter(user_id=self.user.pk, status='CART')
        if not items_to_update.exists():
            raise UnexpectedItemError("User can not make an order from empty cart")

        total_orders_price = model.objects.get_total_products_information(self.user.pk, ['CART'])
        items_objects = Book.objects.all()
        personal_orders_id = uuid.uuid4()
        orders_time = datetime.now()
        city = data.get('city')
        address = data.get('address')

        updated_fields = {
            'order_id': personal_orders_id,
            'orders_time': orders_time,
            'city': city,
            'address': address,
            'total_orders_price': total_orders_price['persons_discounted_price']
        }

        if all([item.amount <= items_objects.get(id=item.book_id).in_stock for item in items_to_update]):

            for item in items_to_update:
                instance = Book.objects.get(id=item.book_id)
                instance.in_stock -= item.amount
                instance.save()

            updated_fields['status'] = 'AWAITING_PAYMENT'
            items_to_update.update(**updated_fields)
        else:
            updated_fields['status'] = 'AWAITING_ARRIVAL'
            items_to_update.update(**updated_fields)

        updated_datas = Cart.objects.filter(**updated_fields).values()

        returned_data = Cart.objects.get_total_orders_information(
            self.user.pk, order_id=updated_fields['order_id']
        )

        for index, product in enumerate(returned_data['products']):
            product.update(updated_datas[index])

        return returned_data

    def update_cart(self, data, *args, **kwargs):
        serializer = CartItemSerializer(data=data["cart"], many=True)
        serializer.is_valid(raise_exception=True)

        data = data["cart"]
        item_in_cart = Cart.objects.filter(status="CART", user_id=self.user.pk)
        returned_data = []

        for item in data:
            product = item_in_cart.filter(book_id=item['book_id'])

            if item["amount"] == 0 and product.exists():
                product.delete()
                continue

            if item["amount"] == 0 and not product.exists():
                continue

            found_item, is_created = Cart.objects.get_or_create(
                status='CART',
                book_id=item['book_id'],
                user_id=self.user.pk,
                warranty_days=14
            )

            found_item.amount = item["amount"]
            found_item.save()
            returned_data.append(found_item)

        return returned_data
