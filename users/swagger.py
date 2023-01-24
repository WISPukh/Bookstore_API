from rest_framework.serializers import Serializer, EmailField, CharField, BooleanField


class SwaggerCreateUserRepresentation(Serializer):  # noqa
    email = EmailField()
    password = CharField()


class SwaggerUserExistsRepresentation(Serializer):  # noqa
    result = BooleanField()
