import django_filters
from django.db.models import QuerySet

from .models import Income


class IncomeFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ("-date", "Newest"),
        ("date", "Oldest"),
        ("-amount", "Highest Amount"),
        ("amount", "Lowest Amount"),
    )

    sort_by = django_filters.ChoiceFilter(
        label="Sort By", choices=SORT_CHOICES, method="filter_sort"
    )
    min_amount = django_filters.NumberFilter(
        field_name="amount", lookup_expr="gte", label="Min Amount"
    )
    max_amount = django_filters.NumberFilter(
        field_name="amount", lookup_expr="lte", label="Max Amount"
    )

    start_date = django_filters.DateFilter(
        field_name="date", lookup_expr="gte", label="Start Date"
    )
    end_date = django_filters.DateFilter(
        field_name="date", lookup_expr="lte", label="End Date"
    )

    class Meta:
        model = Income
        fields = ["sort_by", "min_amount", "max_amount", "start_date", "end_date"]

    def filter_sort(
        self, queryset: QuerySet[Income], name: str, value: str
    ) -> QuerySet[Income]:
        if value:
            return queryset.order_by(value)
        return queryset
