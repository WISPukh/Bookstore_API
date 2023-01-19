from django.db import models

from django.utils.translation import gettext_lazy as _


class Genre(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name=_("Genre's title"),
        unique=True
    )

    description = models.CharField(
        max_length=400,
        verbose_name=_("Genre's description")
    )

    discount = models.IntegerField(
        default=0,
        verbose_name=_('Discount')
    )

    def __str__(self):
        return str(self.title)
