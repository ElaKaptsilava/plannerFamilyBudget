from accounts.models import CustomUser
from budgets_manager.models.budget import BudgetManager
from django.db import models


class SetBudget(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="set_budget"
    )
    budget = models.OneToOneField(BudgetManager, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.budget}"

    def __repr__(self):
        return f"SetBudget(user={self.user.username!r}, budget={self.budget.title!r})"
