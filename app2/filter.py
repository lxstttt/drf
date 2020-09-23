from django_filters import FilterSet
from django_filters import filters

from app2.models import Tree


class TreeFilters(FilterSet):

    min_age = filters.NumberFilter(field_name='age',lookup_expr='gte')
    max_age = filters.NumberFilter(field_name='age',lookup_expr='lte')

    class Meta:
        model = Tree
        fields = ['min_age','max_age']