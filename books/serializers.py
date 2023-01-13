from rest_framework import serializers

from author.models import Author
from genres.models import Genre


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False)
    genres = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all()))
    author = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Author.objects.all()))
    release_date = serializers.DateField(required=False)
