from django.contrib.admin import ModelAdmin, register

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

    def genre(self, obj: Book) -> str:  # noqa
        return '\n'.join([genre.title for genre in obj.genres.all()])

    def authors(self, obj: Book) -> str:  # noqa
        return '\n'.join([author.full_name for author in obj.author.all()])
