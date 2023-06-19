from datetime import datetime
from uuid import uuid4

from books.models import Book
from carts.errors import UnexpectedItemError
from carts.models import Cart


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
        personal_orders_id = uuid4()
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

    def update_cart(self, data):
        data = sorted(data["cart"], key=lambda x: x['book_id'])
        request_book_ids = sorted(item['book_id'] for item in data)

        books = Cart.objects.filter(
            user_id=self.user.pk, status='CART', book_id__in=request_book_ids
        ).order_by('book_id')
        for index, book in enumerate(books):
            book.amount = data[index]['amount']
        Cart.objects.bulk_update(books, ['amount'])

        return books

    def single_update(self, book, data):
        amount = data.get('amount')
        cart = Cart.objects.filter(book_id=book.book_id, user_id=self.user.id)
        cart.update(amount=amount)
        return Cart.objects.get_detailed_information(self.user.id, cart.first().book_id)

    def add_to_cart(self, book, data):
        amount = data.get('amount')

        cart, is_created = Cart.objects.get_or_create(
            user_id=self.user.pk,
            book_id=book.id,
        )
        if is_created:
            cart.amount = amount
        else:
            cart.amount += amount
        cart.save()

        return Cart.objects.get_detailed_information(self.user.id, cart.book_id)
