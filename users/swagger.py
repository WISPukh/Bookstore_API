from rest_framework.serializers import Serializer, EmailField, CharField


class SwaggerCreateUserRepresentation(Serializer):  # noqa
    email = EmailField()
    password = CharField()
