from accounts.models import CustomUser
from budgets_manager.models import BudgetManager
from django.db import models
from django.utils import timezone
from expenses.models import ExpenseCategory


class Expense(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="expenses"
    )
    budget = models.ForeignKey(
        BudgetManager, on_delete=models.CASCADE, related_name="expenses"
    )
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    datetime = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-datetime"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["datetime"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self) -> str:
        return str(self.amount)

    def __repr__(self) -> str:
        return f"Expense(amount={self.amount!r}, user={self.user!r}, category={self.category!r})"
