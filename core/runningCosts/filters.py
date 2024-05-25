"""
List todo:
    filter by:
            - deadline, due_date, payment_deadline, amount, category
            - this month, this year, this week
    sort by:
            - payment_deadline, category, due_date
"""

import django_filters

from .models import RunningCost


class RunningCostFilter(django_filters.FilterSet):
    class Meta:
        model = RunningCost
        fields = []
