from django.db import models

from books.models import Book
from users.models import User


class Favorite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.OneToOneField(Book, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'{self.book_id.title}'
