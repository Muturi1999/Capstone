from rest_framework.pagination import PageNumberPagination

class EventPagination(PageNumberPagination):
    # page size will be one for teststing
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 50
