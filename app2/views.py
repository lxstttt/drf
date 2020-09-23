from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
# Create your views here.
from app2.filter import TreeFilters
from app2.models import Tree
from app2.pagination import PageNumberPagination2, LimitOffsetPagination2, MyCursorPagination
from app2.serializers import TreeModelSerializer
from rest_framework.filters import SearchFilter,OrderingFilter


class TreeAPIView(ListAPIView):

    queryset = Tree.objects.all()
    serializer_class = TreeModelSerializer

    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]

    search_fields = ['age','name','kind']

    order_fields = ['age']

    # 分页器指定
    # pagination_class = PageNumberPagination2
    # pagination_class = LimitOffsetPagination2
    # pagination_class = MyCursorPagination
    filter_class = TreeFilters