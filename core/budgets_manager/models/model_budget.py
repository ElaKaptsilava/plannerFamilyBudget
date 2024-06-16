from decimal import Decimal

from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from incomes.models import Income


class BudgetManager(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        help_text="The user this budget is associated with.",
    )
    savings_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Percentage of the income allocated for savings.",
    )
    wants_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentage of the income allocated for wants.",
    )
    needs_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Percentage of the income allocated for needs.",
    )

    def save(self, *args, **kwargs) -> None:
        total_allocation = (
            self.savings_percentage + self.wants_percentage + self.needs_percentage
        )

        if total_allocation != 100:
            raise ValidationError(
                "The total allocation for saves, wants, and needs must equal 100."
            )
        super().save(*args, **kwargs)

    @property
    def calculate_monthly_income(self) -> Decimal:
        current_month = timezone.now().month
        current_year = timezone.now().year
        total_income = Income.objects.filter(
            user=self.user, date__month=current_month, date__year=current_year
        ).aggregate(total_income=models.Sum("amount"))["total_income"] or Decimal("0.0")
        return total_income

    def update_monthly_income(self):
        self.monthly_income = self.calculate_monthly_income()
        self.save()

    def __str__(self) -> str:
        return f"{self.user.first_name.upper()}'s Budget Plan"

    def __repr__(self) -> str:
        return (
            f"Budget(user={self.user.username!r},"
            f"savings_percentage={self.savings_percentage!r}, wants_percentage={self.wants_percentage!r}, "
            f"needs_percentage={self.needs_percentage!r})"
        )
