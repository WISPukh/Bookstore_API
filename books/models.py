from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from author.models import Author
from genres.models import Genre
from users.models import User


class Book(models.Model):
    quantity = models.IntegerField(
        default=0,
        verbose_name=_('Quantity')
    )

    title = models.CharField(
        max_length=50,
        verbose_name=_('Title')
    )

    description = models.TextField(
        max_length=1000,
        verbose_name=_('Description')
    )

    price = models.IntegerField(
        default=200,
        verbose_name=_('Price')
    )
    #
    # image = models.ImageField(
    #     null=True,
    #     blank=True,
    #     upload_to='',
    #     verbose_name=_('Image')
    # )

    genres = models.ManyToManyField(
        Genre,
        verbose_name='genres'
    )

    author = models.ManyToManyField(
        Author,
        max_length=100,
        verbose_name=_('Author')
    )

    release_date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        default=date.today,
        verbose_name=_('Date of release')
    )

    def __str__(self):
        return str(self.title)

    @property
    def price_discounted(self):
        items_discount = sum([item.get('discount') for item in self.genres.values('discount')])

        return self.price - (items_discount * 0.01) * self.price


class Cart(models.Model):
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
        on_delete=models.DO_NOTHING,
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

    quantity = models.IntegerField(
        null=True,
        verbose_name=_("Quantity")
    )
