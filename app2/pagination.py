from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination


# 基础分页器
class PageNumberPagination2(PageNumberPagination):
    # 指定每页分页的数量
    page_size = 2
    # 修改前端传递每页分页数量的key
    page_size_query_param = "page_size"

    # 指定每页每页的最大数量
    max_page_size = 5
    # 获取第几页的对象  ?page=4: 获取第四页
    page_query_param = "page"


class LimitOffsetPagination2(LimitOffsetPagination):

    default_limit = 4

    limit_query_param = 'limits'

    offset_query_param = 'offsets'

    max_limit = 5


#游标分页器
class MyCursorPagination(CursorPagination):
    cursor_query_param = "cursor"
    page_size = 3
    max_page_size = 5
    # ordering = "price"
    page_size_query_param = "page_size"