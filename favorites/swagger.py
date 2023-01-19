from rest_framework.fields import ListField, IntegerField
from rest_framework.serializers import Serializer


class SwaggerPutRepresentation(Serializer):  # noqa
    book_ids = ListField(child=IntegerField())


class SwaggerCreateRepresentation(Serializer):  # noqa
    book_id = IntegerField()
