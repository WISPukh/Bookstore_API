from rest_framework import serializers

class PaginationLinksSerializer(serializers.Serializer):  # noqa
    next = serializers.URLField(read_only=True)
    previous = serializers.URLField(read_only=True)


class PaginationSerializer(serializers.Serializer):  # noqa
    links = PaginationLinksSerializer()
    total_pages = serializers.IntegerField(read_only=True)
    page = serializers.IntegerField(read_only=True)
    page_size = serializers.IntegerField(read_only=True)
