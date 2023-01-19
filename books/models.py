from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from author.models import Author
from genres.models import Genre
from users.models import User


class Book(models.Model):
    in_stock = models.IntegerField(
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
