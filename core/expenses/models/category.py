from accounts.models import CustomUser
from django.db import models
from expenses.types import Type


class ExpenseCategory(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="expense_categories"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100, default=Type.NEEDS, choices=Type.choices)

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f"ExpenseCategory(name={self.name!r}, type={self.type!r})"
