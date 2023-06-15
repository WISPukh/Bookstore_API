from math import ceil

from django.conf import settings
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
        next_link = self.get_next_link() if self.page.has_next() else None
        previous_link = self.get_previous_link() if self.page.has_previous() else None

        # django's paginator and filters is a black magic, normal way of fixing it unfortunately doesn't work
        if not settings.DEBUG:
            next_link = self.to_https(next_link) if next_link is not None else None
            previous_link = self.to_https(previous_link) if previous_link is not None else None

        return Response(data=self.serializer_class({
            'links': {
                'next': next_link,
                'previous': previous_link
            },
            'total_items': self.page.paginator.count,
            'total_pages': ceil(self.page.paginator.count / self.page_size),
            'page': int(self.request.GET.get('page', 1)),
            'page_size': self.page_size,
            'result': data
        }).data, status=status.HTTP_200_OK)

    @staticmethod
    def to_https(url: str) -> str:
        return url.replace('http', 'https')
