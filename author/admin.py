from django.contrib.admin import ModelAdmin, register

from author.models import Author


@register(Author)
class FavoriteAdmin(ModelAdmin):
    list_display = (
        'first_name',
        'second_name',
        'books'
    )
    ordering = (
        'first_name',
        'second_name',
    )
    search_fields = (
        'first_name',
        'second_name',
    )

    def books(self, obj: Author) -> str:  # noqa
        return ''.join([genre.title for genre in obj.book_set.all()])
