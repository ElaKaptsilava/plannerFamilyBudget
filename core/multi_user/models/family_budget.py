from accounts.models import CustomUser
from budgets_manager.models import BudgetManager
from django.db import models


class FamilyBudget(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="owned_family_budgets"
    )
    members = models.ManyToManyField(CustomUser, related_name="family_budgets")
    budget_manager = models.OneToOneField(BudgetManager, on_delete=models.CASCADE)

    def __str__(self):
        return f"Family Budget owned by {self.owner.email}"

    def __repr__(self):
        return f"FamilyBudget(owner={self.owner.email!r}, budget_manager={self.budget_manager!r})"
