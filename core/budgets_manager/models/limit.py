"""
TODO list:
    1. if elf.type == "wants"
"""

from accounts.models import CustomUser
from budgets_manager.models.budget import BudgetManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "category_running_cost"],
                name="unique_user_category_running_cost",
            ),
            models.UniqueConstraint(
                fields=["user", "category_expense"], name="unique_user_category_expense"
            ),
            models.UniqueConstraint(
                fields=["user", "target"], name="unique_user_target"
            ),
        ]

    @property
    def within_limit(self) -> str:
        total_spent = self.__calculate_total_spent()
        if total_spent < float(self.amount):
            return "bg-info"
        if total_spent > float(self.amount):
            return "bg-danger"
        return "bg-warning"

    @property
    def limit_percentage(self) -> float:
        return self.__calculate_total_spent() * 100 / float(self.amount)

    def __calculate_total_spent(self) -> float:
        today = timezone.now()
        total_spent = 0
        if self.type == "needs":
            if self.category_expense:
                total_spent += (
                    self.user.expenses_set.filter(
                        category=self.category_expense,
                        datetime__year=today.year,
                        datetime__month=today.month,
                    ).aggregate(models.Sum("amount"))["amount__sum"]
                    or 0
                )
            elif self.category_running_cost:
                current_costs = self.user.running_cost_set.filter(
                    next_payment_date__year=today.year,
                    next_payment_date__month=today.month,
                    category=self.category_running_cost,
                )
                for current_cost in current_costs:
                    if not current_cost.is_completed:
                        total_spent += current_cost.total_amount_in_month
        elif self.type == "wants":
            targets = self.user.target_set.filter(
                deadline__gte=today.date(), target=self.target.target
            )
            for target in targets:
                total_spent += float(target.monthly_payment)
        return total_spent

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
