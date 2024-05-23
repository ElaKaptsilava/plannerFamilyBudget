from accounts.models import CustomUser
from django.db import models
from django.utils import timezone


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f"ExpenseCategory(name={self.name!r})"


class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return str(self.amount)

    def __repr__(self) -> str:
        return f"Expense(amount={self.amount!r}, user={self.user!r}, category={self.category!r})"

    class Meta:
        ordering = ["-datetime"]
