from decimal import Decimal

from budgets_manager.models import BudgetManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class MonthlyIncomes(models.Model):
    budget = models.ForeignKey(BudgetManager, on_delete=models.CASCADE)
    year = models.IntegerField(help_text="Enter Year", null=True, blank=True)
    month = models.IntegerField(
        help_text="Enter Month",
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        null=True,
        blank=True,
    )
    total_income = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), null=True, blank=True
    )

    class Meta:
        unique_together = ["budget", "year", "month"]
        ordering = ["budget", "year", "month"]
