from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math


class BookstorePagination(PageNumberPagination):
    page_size = 20
    max_page_size = 1000
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        if self.request.query_params.get('page_size'):
            self.page_size = int(self.request.query_params.get('page_size'))

        super().get_paginated_response(data)
