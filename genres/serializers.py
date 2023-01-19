from rest_framework.serializers import ModelSerializer

from genres.models import Genre


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
