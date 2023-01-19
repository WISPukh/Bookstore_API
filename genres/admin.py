from django.contrib.admin import ModelAdmin, register

from .models import Genre


@register(Genre)
class GenreAdmin(ModelAdmin):
    list_display = ('title', 'description', 'discount')
    ordering = ('id', 'title')
    search_fields = ('title',)
