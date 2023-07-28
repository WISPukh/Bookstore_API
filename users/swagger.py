from rest_framework.serializers import Serializer, EmailField, CharField, BooleanField


class SwaggerCreateUserRepresentation(Serializer):  # noqa
    email = EmailField()
    password = CharField()


class SwaggerUserExistsRepresentation(Serializer):  # noqa
    is_available = BooleanField()


class SwaggerUserExistsRequirements(Serializer):  # noqa
    email = EmailField()
