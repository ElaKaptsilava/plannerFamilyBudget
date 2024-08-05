from budgets_manager.models import BudgetManager
from django.db import models


class Invitation(models.Model):
    budget = models.ForeignKey(
        BudgetManager, on_delete=models.CASCADE, help_text="Enter BudgetManager"
    )
    email = models.EmailField(help_text="Enter Email")
    token = models.CharField(max_length=100, unique=True, help_text="Token")
    accepted = models.BooleanField(default=False, help_text="Is accepted...")

    def __str__(self) -> str:
        return f"Invite to {self.budget.name} for {self.email}"

    def __repr__(self) -> str:
        return f"Invitation(budget={self.budget}, email={self.email})"
