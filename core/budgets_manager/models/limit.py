from budgets_manager import constants
from django.core.exceptions import ValidationError
from django.db import models
from expenses.models import ExpenseCategory
from expenses.types import Type
from runningCosts.models import RunningCostCategory
from targets.models import Target

from core.constants import labels

from .budget import BudgetManager
from .proxy_model_needs import NeedsManager
from .proxy_model_wants import WantsManager


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

    def __str__(self) -> str:
        return f"{self.budget_manager}'s Limit - {self.type} - {self.amount}"

    def __repr__(self) -> str:
        return f"Limit(user={self.budget_manager!r}, type={self.type!r}, amount={self.amount!r})"

    def save(self, *args, **kwargs) -> None:
        self.__validate_budget_type()
        self.__validate_amount()
        super().save(*args, **kwargs)

    def __validate_budget_type(self):
        if self.type == Type.NEEDS:
            if not self.category_expense and not self.category_running_cost:
                raise ValidationError(
                    "For 'needs' type, either category expense or category running cost must be set."
                )
        elif self.type == Type.WANTS:
            if not self.category_expense and not self.category_running_cost:

                raise ValidationError(
                    "For 'wants' type, target or category expense must be set."
                )

    def __validate_amount(self):
        limits = {
            Type.NEEDS: NeedsManager.objects.get(pk=self.budget_manager.pk).get_limit,
            Type.WANTS: WantsManager.objects.get(pk=self.budget_manager.pk).get_limit,
        }
        if self.amount > limits.get(self.type):
            raise ValidationError(
                f"The amount should be less than the {int(limits.get(self.type))}..."
            )

    @property
    def within_limit(self) -> bool:
        return self.calculate_total_spent() < float(self.amount)

    @property
    def spent_percentage(self) -> float:
        return round(self.calculate_total_spent() * 100 / float(self.amount))

    @property
    def spent_percentage_label(self) -> str:
        if self.spent_percentage < constants.WARNING_THRESHOLD:
            return labels.INFO
        elif self.spent_percentage < constants.DANGER_THRESHOLD:
            return labels.WARNING
        return labels.DANGER

    @property
    def within_limit_label(self) -> str:
        if self.within_limit:
            return labels.INFO
        return labels.DANGER

    def calculate_total_spent(self) -> float:
        if self.category_expense:
            return self.total_spent_on_category_expense()
        elif self.type == Type.NEEDS and self.category_running_cost:
            return self.total_spent_on_category_running_cost()
        elif self.type == Type.WANTS and self.target:
            return self.total_wants_spent()

    def total_spent_on_category_running_cost(self) -> float:
        current_costs = self.category_running_cost.running_costs.filter(
            next_payment_date__range=self.budget_manager.get_current_month_range(),
        )
        total_spent = sum(
            current_cost.total_amount_in_month
            for current_cost in current_costs
            if not current_cost.is_completed
        )
        return total_spent or 0.0

    def total_spent_on_category_expense(self) -> float:
        expenses = self.budget_manager.get_monthly_expenses().filter(
            category=self.category_expense
        )
        total = expenses.aggregate(total=models.Sum("amount"))["total"] or 0.0
        return total

    def total_wants_spent(self) -> float:
        filtered_target_contributions = self.target.targetcontribution_set.filter(
            date__range=self.budget_manager.get_current_month_range(),
        )
        total = (
            filtered_target_contributions.aggregate(total=models.Sum("amount"))["total"]
            or 0.0
        )
        return total
