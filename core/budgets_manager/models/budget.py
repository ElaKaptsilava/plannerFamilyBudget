from decimal import Decimal

from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from expenses.models import Expense
from incomes.models import Income


class BudgetManager(models.Model):
    TODAY = timezone.now()
    MAX_ALLOCATION = 100
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        help_text="The user this budget is associated with.",
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

    def save(self, *args, **kwargs) -> None:
        total_allocation = (
            self.savings_percentage + self.wants_percentage + self.needs_percentage
        )

        if total_allocation != self.MAX_ALLOCATION:
            raise ValidationError(
                "The total allocation for saves, wants, and needs must equal 100."
            )
        super().save(*args, **kwargs)

    def _get_current_year_incomes(self) -> QuerySet[Income]:
        current_incomes = Income.objects.filter(
            user=self.user, date__year=self.TODAY.year
        )
        return current_incomes

    @property
    def calculate_monthly_incomes(self) -> Decimal:
        monthly_incomes = self._get_current_year_incomes().filter(
            date__month=self.TODAY.month, date__year=self.TODAY.year
        ).aggregate(monthly_incomes=models.Sum("amount"))["monthly_incomes"] or Decimal(
            "0.0"
        )
        return monthly_incomes

    @property
    def calculate_annual_incomes(self) -> Decimal:
        annual_incomes = self._get_current_year_incomes().aggregate(
            annual_incomes=models.Sum("amount")
        )["annual_incomes"] or Decimal("0.0")
        return annual_incomes

    @property
    def calculate_monthly_expenses(self) -> float:
        get_filtered_expenses = Expense.objects.filter(
            user=self.user,
            datetime__year=self.TODAY.year,
            datetime__month=self.TODAY.month,
        )
        total = (
            get_filtered_expenses.aggregate(total=models.Sum("amount"))["total"]
            or Decimal()
        )
        return total

    def __str__(self) -> str:
        return f"{self.user.first_name.upper()}'s Budget Plan"

    def __repr__(self) -> str:
        return (
            f"Budget(user={self.user.username!r},"
            f"savings_percentage={self.savings_percentage!r}, wants_percentage={self.wants_percentage!r}, "
            f"needs_percentage={self.needs_percentage!r})"
        )
