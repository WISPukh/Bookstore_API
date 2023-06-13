from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import UserSerializer
from .swagger import SwaggerCreateUserRepresentation, SwaggerUserExistsRepresentation


class UsersViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    model = User
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get']

    @swagger_auto_schema(
        request_body=SwaggerCreateUserRepresentation, responses={200: openapi.Response('', schema=serializer_class)}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('email', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)],
        responses={200: openapi.Response(
            'Checks if user with given email exists', schema=SwaggerUserExistsRepresentation
        )}
    )
    @action(methods=['get'], detail=False, url_path='available')
    def exists(self, request, *args, **kwargs):
        email = self.request.query_params.get('email')
        return Response({'is_available': not self.model.objects.filter(email=email).exists()})

    @action(methods=['get'], detail=False, url_path='me', permission_classes=[IsAuthenticated])
    def get_object(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.request.user).data)

