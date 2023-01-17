from django.db import models


class Author(models.Model):
    first_name = models.CharField('First name', max_length=20)
    second_name = models.CharField('Second name', max_length=20)
