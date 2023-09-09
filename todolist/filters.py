import django_filters
from django.contrib.auth.models import User

from todolist.models import Task


class TaskFilter(django_filters.FilterSet):
    user = django_filters.CharFilter()
    username = django_filters.CharFilter(field_name='user__username')

    class Meta:
        model = User
        fields = ('user', 'username')
