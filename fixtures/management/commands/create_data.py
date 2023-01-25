from datetime import timedelta
from random import randint, choice

from django.core.management.base import BaseCommand
from factory import Faker, Sequence
from factory.django import DjangoModelFactory

from author.models import Author
from books.models import Book
from genres.models import Genre


def get_price():
    return randint(499, 9999)


def get_in_stock():
    return randint(1, 100)


def get_discount():
    return randint(0, 100)


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    first_name = Faker('first_name')
    second_name = Faker('last_name')


class GenreFactory(DjangoModelFactory):
    class Meta:
        model = Genre

    title = Faker('name')
    description = Faker('text')
    discount = Sequence(lambda _: get_discount())


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    in_stock = Sequence(lambda _: get_in_stock())
    title = Faker('name')
    description = Faker('text')
    price = Sequence(lambda _: get_price())
    release_date = Faker('date_object')


class Command(BaseCommand):
    def handle(self, *args, **options):
        authors = [AuthorFactory() for _ in range(100)]
        genres = [GenreFactory() for _ in range(100)]
        for i in range(100):
            book = BookFactory()
            book.genres.add(choice(genres))
            book.writing_date = book.release_date - timedelta(days=randint(365, 365 * 3), weeks=randint(10, 40))

            # book can have no authors or more than 3
            for j in range(randint(0, 3)):
                book.author.add(choice(authors))

            book.save()
