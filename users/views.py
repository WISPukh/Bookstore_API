from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer
from .swagger import SwaggerCreateUserRepresentation


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    @swagger_auto_schema(
        request_body=SwaggerCreateUserRepresentation, responses={200: openapi.Response('', schema=serializer_class)}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
