from django.contrib.admin import ModelAdmin, register
from django.utils.safestring import mark_safe

from books.models import Book


@register(Book)
class BookAdmin(ModelAdmin):
    list_display = (
        'title',
        'description',
        'price',
        'in_stock',
        'genre',
        'authors',
        'release_date'
    )
    ordering = (
        'title',
        'description',
        'price',
        'in_stock',
        'release_date'
    )
    search_fields = ('title',)
    readonly_fields = ['preview']

    def preview(self, book: Book) -> str:  # noqa
        if book.preview_image.url:
            return mark_safe(f"<img src='{book.preview_image.url}'>")
        return 'No image'

    def genre(self, book: Book) -> str:  # noqa
        return '\n'.join([genre.title for genre in book.genres.all()])

    def authors(self, book: Book) -> str:  # noqa
        return '\n'.join([author.full_name for author in book.author.all()])
