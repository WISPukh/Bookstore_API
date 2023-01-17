from django.db import models
from django.utils.translation import gettext_lazy as _

from carts.managers import CartManager
from users.models import User
from books.models import Book


class Cart(models.Model):
    objects = CartManager()

    class Status(models.TextChoices):
        CART = 'CART', _('In cart')
        AWAITING_ARRIVAL = 'AWAITING_ARRIVAL', _('Awaiting_arrival')
        AWAITING_PAYMENT = 'AWAITING_PAYMENT', _('Awaiting payment')
        PAID = 'PAID', _('Paid')
        AWAITING_DELIVERY = 'AWAITING_DELIVERY', _('Awaiting delivery')
        SENT = 'SENT', _('Sent')
        FINISHED = 'FINISHED', _('Finished')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        default=1,
        verbose_name=_('User')
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        blank=True,
        default=1,
        verbose_name=_('Item')
    )

    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default='CART',
        verbose_name=_('State')
    )

    order_id = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name=_("Order's id")
    )

    amount = models.IntegerField(
        null=True,
        verbose_name=_("Quantity")
    )

    warranty_days = models.IntegerField(
        "Dates of warranty",
        default=30
    )

    orders_time = models.DateTimeField(
        "Orders date time field",
        null=True,
        blank=True
    )

    city = models.CharField(
        'Delivery city',
        max_length=100,
        default='12345'
    )

    address = models.CharField(
        'Delivery address',
        max_length=250,
        default='12345'
    )

    total_orders_price = models.IntegerField(
        "Total price of order",
        null=True,
        blank=True
    )
