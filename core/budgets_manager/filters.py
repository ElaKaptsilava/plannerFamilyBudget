import django_filters
from budgets_manager.models import LimitManager
from django.db.models import QuerySet


class LimitFilterSet(django_filters.FilterSet):
    PROGRESS_CHOICES = [("80", "Warning"), ("100", "Danger")]
    progres_filter = django_filters.ChoiceFilter(
        choices=PROGRESS_CHOICES, method="filter_by_progress", label="Progress"
    )

    class Meta:
        model = LimitManager
        fields = [
            "type",
        ]

    def filter_by_progress(self, queryset, name, value) -> QuerySet:
        if value == "100":
            filtered_queryset = [
                limit.pk for limit in queryset if limit.limit_percentage > 100
            ]
        elif value == "80":
            filtered_queryset = [
                limit.pk for limit in queryset if 80 <= limit.limit_percentage <= 100
            ]
        else:
            return queryset
        return queryset.model.objects.filter(pk__in=filtered_queryset)
