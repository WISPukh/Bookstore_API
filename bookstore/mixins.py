from bookstore.pagination import BookstorePagination


class PaginationViewSetMixin:
    """
    ___________________________________
    Implements ModelViewSet list method
    ___________________________________
    """
    pagination_class = BookstorePagination
    pagination_serializer_class = None

    def list(self, request, *args, **kwargs):
        if not self.pagination_serializer_class:
            raise AttributeError(
                f'Attribute "pagination_serializer_class" must be included in {self.__class__.__name__}'
            )
        queryset = self.paginate_queryset(self.get_queryset())
        self.pagination_class.serializer_class = self.pagination_serializer_class
        return self.get_paginated_response(queryset)
