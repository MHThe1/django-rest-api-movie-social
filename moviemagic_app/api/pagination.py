from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 10
    

class WatchListLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
    offset_query_param = 'start'
    
    
class WatchListCursorPagination(CursorPagination):
    page_size = 5
    ordering = 'created'