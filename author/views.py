from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from bookstore.mixins import ItemsViewSetMixin
from bookstore.permissions import IsAdminUserOrReadOnly
from .models import Author
from .serializers import AuthorSerializer, PaginationAuthorSerializer, SuggestionList


class AuthorViewSet(ItemsViewSetMixin):
    model = Author

    serializer_class = AuthorSerializer
    pagination_serializer_class = PaginationAuthorSerializer
    http_method_names = ['get', 'patch', 'delete', 'post']
    permission_classes = (IsAdminUserOrReadOnly, )

    def get_queryset(self):
        return Author.objects.all()


class AuthorSuggestionViewSet(GenericViewSet):
    serializer_class = SuggestionList
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'second_name']
    http_method_names = ['get']

    def get_queryset(self):
        return Author.objects.all()

    @action(methods=['get'], detail=False, url_path='suggestion')
    def get_list_short(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(self.serializer_class(queryset, many=True).data, status=200)
