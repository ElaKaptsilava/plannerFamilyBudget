import django_filters

from .models import Expense, ExpenseCategory


class ExpenseFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ("-datetime", "Newest"),
        ("datetime", "Oldest"),
        ("-amount", "Highest Amount"),
        ("amount", "Lowest Amount"),
    )

    sort_by = django_filters.ChoiceFilter(
        label="Sort By", choices=SORT_CHOICES, method="filter_sort"
    )
    category = django_filters.ModelChoiceFilter(
        queryset=ExpenseCategory.objects.all(), label="Category"
    )

    min_amount = django_filters.NumberFilter(
        field_name="amount", lookup_expr="gte", label="Min Amount"
    )
    max_amount = django_filters.NumberFilter(
        field_name="amount", lookup_expr="lte", label="Max Amount"
    )

    start_date = django_filters.DateFilter(
        field_name="datetime", lookup_expr="gte", label="Start Date"
    )
    end_date = django_filters.DateFilter(
        field_name="datetime", lookup_expr="lte", label="End Date"
    )

    class Meta:
        model = Expense
        fields = []

    def filter_sort(self, queryset, name, value):
        if value:
            return queryset.order_by(value)
        return queryset
