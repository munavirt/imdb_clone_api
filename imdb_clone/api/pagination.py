from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'p'  #you can change parameters using this page to p
    page_size_query_param = 'size'#client overwrite this parameter



class WatchListOSPagination(LimitOffsetPagination):
    default_limit = 4
    max_limit = 3


class WatchListCPagination(CursorPagination):
    page_size = 3
    ordering = 'created'
    cursor_query_param = 'record'