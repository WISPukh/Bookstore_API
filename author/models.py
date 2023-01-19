from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    first_name = models.CharField(
        max_length=40,
        verbose_name=_('First name')
    )
    second_name = models.CharField(
        max_length=40,
        verbose_name=_('Second Name')
    )

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name}  {self.second_name}"
