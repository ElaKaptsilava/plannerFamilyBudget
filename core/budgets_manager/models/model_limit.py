from accounts.models import CustomUser
from budgets_manager.models.model_budget import BudgetManager
from django.core.exceptions import ValidationError
from django.db import models
from expenses.models import ExpenseCategory
from runningCosts.models import RunningCostCategory
from targets.models import Target


class LimitManager(models.Model):
    BUDGET_TYPE_CHOICES = [
        ("", "Select Type"),
        ("wants", "Wants"),
        ("needs", "Needs"),
    ]
    user = models.ForeignKey(
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
        return f"{self.user.username}'s Limit - {self.type} - {self.amount}"

    def __repr__(self) -> str:
        return f"Limit(user={self.user.username!r}, save={self.type!r}, amount={self.amount!r})"
