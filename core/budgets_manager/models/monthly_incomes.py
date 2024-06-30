from datetime import datetime

from budgets_manager.models import BudgetManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from incomes.models import Income


class MonthlyIncomes(models.Model):
    budget = models.ForeignKey(BudgetManager, on_delete=models.CASCADE)
    year = models.IntegerField(
        help_text="Enter Year",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year + 100),
        ],
    )
    month = models.IntegerField(
        help_text="Enter Month",
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ["budget", "year", "month"]
        ordering = ["budget", "year", "month"]

    @property
    def total_incomes_sum(self) -> dict:
        incomes = Income.objects.filter(
            user=self.budget.user, date__year=self.year, date__month=self.month
        )
        total = incomes.aggregate(total=models.Sum("amount"))["total"]
        return total
