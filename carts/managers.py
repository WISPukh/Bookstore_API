from typing import Optional

from django.db import models

from books.models import Book
from users.models import User


class CartManager(models.Manager):

    # FOR Cart.

    def get_personal_discount(self, user_pk):  # noqa
        return User.objects.filter(id=user_pk).first().personal_discount * 0.01

    def get_detailed_information(self, user_pk, book_id) -> Optional[dict]:
        product = self.filter(user_id=user_pk, status='CART', book_id=book_id)

        if not product:
            return None

        product = product.values().first()
        new_price = Book.objects.get(id=product.get('book_id')).price_discounted

        product['price_discounted'] = product['amount'] * new_price
        product['new_price'] = new_price

        return product

    def total_price_discounted(self, user_pk, status):

        for product in self.filter(user_id=user_pk, status__in=status).order_by('id').values():  # noqa
            new_price = Book.objects.get(
                id=product['book_id']
            ).price_discounted

            product['price_discounted'] = product['amount'] * new_price
            product['new_price'] = new_price
            yield product

    def get_total_products_information(self, user_pk, status):
        extra_products = list(self.total_price_discounted(user_pk, status))
        total = sum(
            field['price_discounted']
            for field in extra_products
        )
        return dict(
            total=total,
            persons_discounted_price=total - self.get_personal_discount(user_pk) * total,
            products=extra_products
        )

    # FOR Order.

    def get_status(self, order_id):
        return self.filter(order_id=order_id).first().status

    def set_discounted_price_inf(self, order_id, user_pk):

        for product in self.filter(user_id=user_pk, order_id=order_id).order_by('id').values():  # noqa
            product_discounted_price = Book.objects.get(
                id=product['book_id']).price_discounted

            product['price_discounted'] = product['amount'] * product_discounted_price
            product['new_price'] = product_discounted_price

            yield product

    def get_total_orders_information(self, user_pk, order_id):
        extra_products = list(self.set_discounted_price_inf(order_id, user_pk))
        total = sum(
            field['price_discounted']
            for field in extra_products
        )
        return dict(
            order_id=order_id,
            status=self.get_status(order_id),
            total=total,
            persons_discounted_price=total - self.get_personal_discount(user_pk) * total,
            products=extra_products
        )
