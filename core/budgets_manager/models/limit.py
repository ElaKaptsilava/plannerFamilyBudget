from budgets_manager import constants
from budgets_manager.models import BudgetManager
from django.core.exceptions import ValidationError
from django.db import models
from expenses.models import ExpenseCategory
from expenses.types import Type
from runningCosts.models import RunningCostCategory
from targets.models import Target

from core.constants import labels


class LimitManager(models.Model):
    budget_manager = models.ForeignKey(BudgetManager, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=10, choices=Type.choices, help_text="Type of budget category."
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
        if self.limit_percentage < constants.WARNING_THRESHOLD:
            return labels.DANGER if self.type == Type.WANTS else labels.INFO
        elif self.limit_percentage <= constants.DANGER_THRESHOLD:
            return labels.WARNING
        return labels.DANGER if self.type == Type.WANTS else labels.SUCCESS

    @property
    def within_limit_label(self) -> str:
        if self.within_limit:
            return labels.INFO
        return labels.DANGER

    def _calculate_total_spent(self) -> float:
        if self.type == Type.NEEDS:
            if self.category_expense:
                return self._calculate_total_spent_for_category_expense()
            elif self.category_running_cost:
                return self._calculate_total_spent_for_category_running_cost()
        elif self.type == Type.WANTS:
            return self._calculate_wants_spent()

    def _calculate_total_spent_for_category_running_cost(self) -> float:
        current_costs = self.category_running_cost.running_costs.filter(
            next_payment_date__year=constants.TODAY.year,
            next_payment_date__month=constants.TODAY.month,
        )
        total_spent = sum(
            current_cost.total_amount_in_month
            for current_cost in current_costs
            if not current_cost.is_completed
        )
        return total_spent or 0.0

    def _calculate_total_spent_for_category_expense(self) -> float:
        filtered_expenses = self.budget_manager.user.expense_set.filter(
            category=self.category_expense,
            datetime__year=constants.TODAY.year,
            datetime__month=constants.TODAY.month,
        )
        total = filtered_expenses.aggregate(total=models.Sum("amount"))["total"] or 0.0
        return total

    def _calculate_wants_spent(self) -> float:
        filtered_target_contributions = self.target.targetcontribution_set.filter(
            date__year=constants.TODAY.year,
            date__month=constants.TODAY.month,
        )
        total = (
            filtered_target_contributions.aggregate(total=models.Sum("amount"))["total"]
            or 0.0
        )
        return total

    def save(self, *args, **kwargs) -> None:
        self.__validate_budget_type()
        super().save(*args, **kwargs)

    def __validate_budget_type(self):
        if self.type == Type.NEEDS and not (
            self.category_expense or self.category_running_cost
        ):
            raise ValidationError(
                "For 'needs' type, either category_expense or category_running_cost must be set."
            )
        elif self.type == Type.WANTS and not self.target:
            raise ValidationError("For 'wants' type, target must be set.")

    def __str__(self) -> str:
        return (
            f"{self.budget_manager.user.username}'s Limit - {self.type} - {self.amount}"
        )

    def __repr__(self) -> str:
        return f"Limit(user={self.budget_manager.user.username!r}, type={self.type!r}, amount={self.amount!r})"
