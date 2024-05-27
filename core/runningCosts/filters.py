"""
List todo:
    filter by:
            - due_date, payment_deadline, amount, category
            - this month, this year, this week
"""

import django_filters
from django.db.models import QuerySet
from django.utils import timezone

from .models import RunningCost

SORT_CHOICES = (
    ("-payment_deadline", "Payment deadline Descending"),
    ("payment_deadline", "Payment deadline Ascending"),
    ("-amount", "Highest Amount"),
    ("amount", "Lowest Amount"),
    ("-due_date", "Due Date Descending"),
    ("due_date", "Due Date Ascending"),
)

TIME_PERIOD_CHOICES = (
    ("this_month", "This Month"),
    ("this_year", "This Year"),
    ("this_week", "This Week"),
    ("this_day", "This Day"),
)


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

    def filter_sort(
        self, queryset: QuerySet[RunningCost], name: str, value: str
    ) -> QuerySet[RunningCost]:
        if value:
            return queryset.order_by(value)
        return queryset

    def filter_by_time_period(
        self, queryset: QuerySet[RunningCost], name: str, value: str
    ) -> QuerySet[RunningCost]:
        now = timezone.now()
        filter_queryset_by_values = {
            "this_month": queryset.filter(payment_deadline__month=now.month),
            "this_year": queryset.filter(payment_deadline__year=now.year),
            "this_week": queryset.filter(payment_deadline__week=now.isocalendar().week),
            "this_day": queryset.filter(payment_deadline__day=now.day),
        }
        return filter_queryset_by_values.get(value)
