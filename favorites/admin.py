from django.contrib.admin import ModelAdmin, register

from favorites.models import Favorite


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user_id', 'book_id')
    ordering = ('user_id', 'book_id')
    search_fields = ('user_id', 'book_id')
    list_filter = ('user_id',)
