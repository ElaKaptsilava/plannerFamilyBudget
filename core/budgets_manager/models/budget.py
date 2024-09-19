from accounts.models.user import CustomUser
from budgets_manager import constants
from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class BudgetManager(models.Model):
    TODAY = constants.TODAY
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        help_text="The user this budget is associated with.",
    )
    title = models.CharField(max_length=50, default="Family")
    color = ColorField(default="#FF0000")
    participants = models.ManyToManyField(
        CustomUser, related_name="participants", default=list
    )
    savings_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Percentage of the income allocated for savings.",
    )
    wants_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentage of the income allocated for wants.",
    )
    needs_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Percentage of the income allocated for needs.",
    )

    def __str__(self) -> str:
        return f"{self.user.first_name.upper()}'s Budget Plan"

    def __repr__(self) -> str:
        return (
            f"Budget(user={self.user.username!r},"
            f"savings_percentage={self.savings_percentage!r}, wants_percentage={self.wants_percentage!r}, "
            f"needs_percentage={self.needs_percentage!r})"
        )

    def clean(self):
        allocation = (
            self.savings_percentage + self.needs_percentage + self.wants_percentage
        )
        if allocation != constants.MAX_ALLOCATION:
            raise ValidationError(
                "The total allocation for savings, needs, and wants must equal 100."
            )

    def get_annual_incomes(self) -> QuerySet:
        return self.incomes.filter(
            user__in=self.participants.all(), date__year=self.TODAY.year
        )

    def get_monthly_incomes(self) -> QuerySet:
        return self.get_annual_incomes().filter(date__month=self.TODAY.month)

    def get_annual_expenses(self) -> QuerySet:
        return self.expenses.filter(
            user__in=self.participants.all(), datetime__year=self.TODAY.year
        )

    def get_monthly_expenses(self) -> QuerySet:
        return self.get_annual_expenses().filter(datetime__month=self.TODAY.month)

    def get_month_range(self):
        start_date = self.TODAY.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        end_date = start_date.replace(month=start_date.month + 1) - timezone.timedelta(
            microseconds=1
        )
        return start_date, end_date

    @property
    def total_monthly_incomes(self) -> float:
        total = self.get_monthly_incomes().aggregate(total=models.Sum("amount"))[
            "total"
        ]
        return float(total) if total else 0.0

    @property
    def total_annual_incomes(self) -> float:
        total = self.get_annual_incomes().aggregate(total=models.Sum("amount"))["total"]
        return float(total) if total else 0.0

    @property
    def total_monthly_expenses(self) -> float:
        total = self.get_monthly_expenses().aggregate(total=models.Sum("amount"))[
            "total"
        ]
        return total if total else 0.0
