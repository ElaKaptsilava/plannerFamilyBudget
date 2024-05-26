"""
List todo:
    filter by:
            - due_date, payment_deadline, amount, category
            - this month, this year, this week
"""

import django_filters
from django.utils import timezone

from .constants import SORT_CHOICES, TIME_PERIOD_CHOICES
from .models import RunningCost


class RunningCostFilter(django_filters.FilterSet):
    sort_by = django_filters.ChoiceFilter(
        label="Sort By", choices=SORT_CHOICES, method="filter_sort"
    )
    deadline_time = django_filters.ChoiceFilter(
        label="Time Period", choices=TIME_PERIOD_CHOICES, method="filter_by_time_period"
    )

    class Meta:
        model = RunningCost
        fields = ["deadline_time", "sort_by"]

    def filter_sort(self, queryset, name, value):
        if value:
            return queryset.order_by(value)
        return queryset

    def filter_by_time_period(self, queryset, name, value):
        now = timezone.now()
        filter_queryset_by_values = {
            "this_month": queryset.filter(payment_deadline__month=now.month),
            "this_year": queryset.filter(payment_deadline__year=now.year),
            "this_week": queryset.filter(payment_deadline__week=now.isocalendar().week),
            "this_day": queryset.filter(payment_deadline__day=now.day),
        }
        return filter_queryset_by_values.get(value)
