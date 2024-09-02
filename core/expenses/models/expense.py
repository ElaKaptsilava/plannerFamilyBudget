from accounts.models import CustomUser
from django.db import models
from django.utils import timezone
from expenses.models import ExpenseCategory


class Expense(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="expenses"
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

    # def save(self, *args, **kwargs) -> None:
    #     self.__check_limit()
    #     super().save(*args, **kwargs)
    # def __check_limit(self):
    #      total_limit = self.user.budgetmanager.limitmanager_set.aggregate(total=models.Sum("amount"))["total"]
    #      if
