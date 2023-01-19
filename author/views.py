from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Author
from .serializers import AuthorSerializer


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_queryset(self):
        return Author.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response_data = self.serializer_class(instance=instance).data
        self.perform_destroy(instance)

        return Response(response_data, status=200)
