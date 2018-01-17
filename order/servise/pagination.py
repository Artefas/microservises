from rest_framework import pagination
from rest_framework.response import Response


class MyPagination(pagination.PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'page_count': self.page.paginator.num_pages,
            'page_size': self.page_size
        })