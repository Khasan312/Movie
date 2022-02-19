from rest_framework.pagination import PageNumberPagination


class PaginationFilms(PageNumberPagination):
    page_size = 2
    max_page_size = 100