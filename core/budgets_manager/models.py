from decimal import Decimal

from django.utils import timezone

from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.db import models
from expenses.models import ExpenseCategory
from incomes.models import Income
from runningCosts.models import RunningCostCategory
from targets.models import Target


class BudgetManager(models.Model):
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
            Decimal(self.savings_percentage)
            + Decimal(self.wants_percentage)
            + Decimal(self.needs_percentage)
        )
        if total_allocation != 100:
            raise ValidationError(
                "The total allocation for saves, wants, and needs must equal 100."
            )
        super().save(*args, **kwargs)

    @property
    def calculate_monthly_income(self):
        current_month = timezone.now().month
        current_year = timezone.now().year
        total_income = Income.objects.filter(
            user=self.user, date__month=current_month, date__year=current_year
        ).aggregate(total_income=models.Sum("amount"))["total_income"] or Decimal("0.0")
        return total_income

    def update_monthly_income(self):
        self.monthly_income = self.calculate_monthly_income()
        self.save()

    def __str__(self) -> str:
        return f"{self.user.first_name.upper()}'s Budget Plan"

    def __repr__(self) -> str:
        return (
            f"Budget(user={self.user.username!r}, monthly_income={self.monthly_income!r}, "
            f"savings_percentage={self.savings_percentage!r}, wants_percentage={self.wants_percentage!r}, "
            f"needs_percentage={self.needs_percentage!r})"
        )


class PlannerManager(models.Model):
    BUDGET_TYPE_CHOICES = [
        ("wants", "Wants"),
        ("needs", "Needs"),
    ]
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        help_text="The user this budget is associated with.",
    )
    budget_manager = models.ForeignKey(BudgetManager, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=10, choices=BUDGET_TYPE_CHOICES, help_text="Type of budget category."
    )
    category_expense = models.OneToOneField(
        ExpenseCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Expense category for 'needs' type budget.",
    )
    category_running_cost = models.OneToOneField(
        RunningCostCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Running cost category for 'needs' type budget.",
    )
    target = models.OneToOneField(
        Target,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Target category for 'wants' type budget.",
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        help_text="Amount allocated to this budget entry.",
    )

    def save(self, *args, **kwargs) -> None:
        if self.type == "needs":
            if not self.category_expense or not self.category_running_cost:
                raise ValidationError(
                    "For 'needs' type, either category_expense or category_running_cost must be set."
                )
        elif self.type == "wants":
            if not self.target:
                raise ValidationError("For 'wants' type, target must be set.")

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username}'s Planer - {self.type} - {self.amount}"

    def __repr__(self) -> str:
        return f"Planer(user={self.user.username!r}, save={self.type!r}, amount={self.amount!r})"