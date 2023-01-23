from math import ceil

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BookstorePagination(PageNumberPagination):
    page_size = 20
    max_page_size = 1000
    page_size_query_param = 'page_size'
    serializer_class = None

    def get_paginated_response(self, data):
        self.page_size = int(self.request.query_params.get('page_size', self.page_size))

        return Response(data=self.serializer_class({
            'links': {
                'next': self.get_next_link() if self.page.has_next() else None,
                'previous': self.get_previous_link() if self.page.has_previous() else None
            },
            'total_items': self.page.paginator.count,
            'total_pages': ceil(self.page.paginator.count / self.page_size),
            'page': int(self.request.GET.get('page', 1)),
            'page_size': self.page_size,
            'result': data
        }).data, status=status.HTTP_200_OK)
