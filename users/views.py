from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']
