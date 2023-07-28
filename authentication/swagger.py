from rest_framework.serializers import Serializer, EmailField, CharField, BooleanField


class SwaggerLoginRequirements(Serializer):  # noqa
    email = EmailField()
    password = CharField()
