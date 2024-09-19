from datetime import datetime

from budgets_manager.models import BudgetManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
    monthly_income = models.IntegerField(default=0)

    class Meta:
        unique_together = ["budget", "year", "month"]
        ordering = ["budget", "year", "month"]

    @property
    def total_incomes_sum(self) -> dict:
        return self.budget.calculate_total_monthly_incomes
