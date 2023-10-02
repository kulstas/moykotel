from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post


class PostsFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='post_date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
       model = Post
       fields = {
           'post_title': ['contains'],
           'post_category': ['exact'],
       }