from django.db import models


class Author(models.Model):
    first_name = models.CharField('First name', max_length=20)
    second_name = models.CharField('Second name', max_length=20)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name}  {self.second_name}"
