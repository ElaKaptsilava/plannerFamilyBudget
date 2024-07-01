from budgets_manager.models import BudgetManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from expenses.models import ExpenseCategory
from runningCosts.models import RunningCostCategory
from targets.models import Target

from core.constants import labels


class LimitManager(models.Model):
    BUDGET_TYPE_CHOICES = [
        ("", "Select Type"),
        ("wants", "Wants"),
        ("needs", "Needs"),
    ]

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

    @property
    def within_limit(self) -> bool:
        return self._calculate_total_spent() < float(self.amount)

    @property
    def limit_percentage(self) -> float:
        return self._calculate_total_spent() * 100 / float(self.amount)

    @property
    def limit_percentage_label(self) -> str:
        if self.limit_percentage < 80:
            return labels.INFO
        elif self.limit_percentage <= 100:
            return labels.WARNING
        return labels.DANGER

    @property
    def within_limit_label(self) -> str:
        if self.within_limit:
            return labels.INFO
        return labels.DANGER

    def _calculate_total_spent(self) -> float:
        today = timezone.now()
        total_spent = 0

        if self.type == "needs":
            total_spent = self._calculate_needs_spent(today)
        elif self.type == "wants":
            total_spent = self._calculate_wants_spent(today)

        return total_spent

    def _calculate_needs_spent(self, today):
        total_spent = 0
        not_choice_any = not self.category_expense and self.category_running_cost
        if self.category_expense or not_choice_any:
            total_spent += (
                self.budget_manager.user.expense_set.filter(
                    category=self.category_expense,
                    datetime__year=today.year,
                    datetime__month=today.month,
                ).aggregate(models.Sum("amount"))["amount__sum"]
                or 0
            )
        elif self.category_running_cost or not_choice_any:
            current_costs = self.category_running_cost.running_costs.filter(
                next_payment_date__year=today.year,
                next_payment_date__month=today.month,
            )
            total_spent += sum(
                current_cost.total_amount_in_month
                for current_cost in current_costs
                if not current_cost.is_completed
            )

        return total_spent

    def _calculate_wants_spent(self, today):
        return self.target.monthly_payment

    def save(self, *args, **kwargs) -> None:
        self._validate_budget_type()
        super().save(*args, **kwargs)

    def _validate_budget_type(self):
        if self.category_expense or self.category_running_cost or self.target:
            if self.type == "needs" and not (
                self.category_expense or self.category_running_cost
            ):
                raise ValidationError(
                    "For 'needs' type, either category_expense or category_running_cost must be set."
                )
            elif self.type == "wants" and not self.target:
                raise ValidationError("For 'wants' type, target must be set.")

    def __str__(self) -> str:
        return (
            f"{self.budget_manager.user.username}'s Limit - {self.type} - {self.amount}"
        )

    def __repr__(self) -> str:
        return f"Limit(user={self.budget_manager.user.username!r}, type={self.type!r}, amount={self.amount!r})"
