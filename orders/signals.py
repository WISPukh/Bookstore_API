from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import Book
from carts.models import Cart
from .tasks import order_created


@transaction.atomic
@receiver(post_save, sender=Book)
def update(sender, instance, update_fields, **kwargs):
    order_awaiting_refill = Cart.objects.filter(
        status='AWAITING_ARRIVAL'
    ).order_by(
        'orders_time'
    ).first()

    if order_awaiting_refill is not None:

        items_amount = Cart.objects.filter(order_id=order_awaiting_refill.order_id).values(
            'book_id', 'amount'
        ).order_by('book_id')

        all_products = Book.objects.filter(id__in=[item['book_id'] for item in items_amount])

        if all(
                [all_products.get(
                    id=item['book_id']
                ).in_stock
                 >= item['amount']
                 for item in items_amount]
        ):
            Cart.objects.filter(order_id=order_awaiting_refill.order_id
                                ).update(
                status='AWAITING_PAYMENT'
            )

            # order_created.delay(
            #     order_id=order_awaiting_refill.order_id
            # )
