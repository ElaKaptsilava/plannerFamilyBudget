from accounts.models import CustomUser
from budgets_manager import constants
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet
from expenses.models import Expense
from incomes.models import Income


class BudgetManager(models.Model):
    TODAY = constants.TODAY
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

        if total_allocation != constants.MAX_ALLOCATION:
            raise ValidationError(
                "The total allocation for saves, wants, and needs must equal 100."
            )
        super().save(*args, **kwargs)

    def _get_current_year_incomes(self) -> QuerySet[Income]:
        return Income.objects.filter(user=self.user, date__year=self.TODAY.year)

    @property
    def calculate_total_monthly_incomes(self) -> float:
        monthly_incomes = self._get_current_year_incomes().filter(
            date__month=self.TODAY.month, date__year=self.TODAY.year
        )
        total = monthly_incomes.aggregate(total=models.Sum("amount"))["total"]
        return float(total) or 0.0

    @property
    def calculate_annual_incomes(self) -> float:
        annual_incomes = self._get_current_year_incomes().aggregate(
            annual_incomes=models.Sum("amount")
        )["annual_incomes"]
        return float(annual_incomes) or 0.0

    @property
    def calculate_monthly_expenses(self) -> float:
        get_filtered_expenses = Expense.objects.filter(
            user=self.user,
            datetime__year=self.TODAY.year,
            datetime__month=self.TODAY.month,
        )
        total = get_filtered_expenses.aggregate(total=models.Sum("amount"))["total"]

        return total or 0.0

    def __str__(self) -> str:
        return f"{self.user.first_name.upper()}'s Budget Plan"

    def __repr__(self) -> str:
        return (
            f"Budget(user={self.user.username!r},"
            f"savings_percentage={self.savings_percentage!r}, wants_percentage={self.wants_percentage!r}, "
            f"needs_percentage={self.needs_percentage!r})"
        )
