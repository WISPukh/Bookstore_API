from django.core.management.base import BaseCommand

from author.models import Author
from books.models import Book
from genres.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        Book.objects.all().delete()
        Author.objects.all().delete()
        Genre.objects.all().delete()
