from django_filters import rest_framework as filters
from django.db.models import ArrayField
from django_filters.filters import BaseInFilter, CharFilter
from .models import Post

class CharArrayFilter(BaseInFilter, CharFilter):
    pass

class PostFilter(filters.FilterSet):
    category = CharArrayFilter(field_name='category', lookup_expr='contains')
    tag = CharArrayFilter(field_name='tag', lookup_expr='contains')

    class Meta:
        model = Post
        fields = ['category', 'tag']
        filter_overrides = {
            ArrayField: {
                'filter_class': CharArrayFilter,
            },
        }
