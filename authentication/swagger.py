from rest_framework.serializers import Serializer, EmailField, CharField, BooleanField


class SwaggerLoginRepresentation(Serializer):  # noqa
    email = EmailField()
    password = CharField()
