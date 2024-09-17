from accounts.models import CustomUser
from budgets_manager.models import BudgetManager
from colorfield.fields import ColorField
from django.db import models


class FamilyBudget(models.Model):
    title = models.CharField(max_length=50, default="Family")
    color = ColorField(default="#FF0000")
    members = models.ManyToManyField(
        CustomUser, related_name="family_budgets", default=list
    )
    budget_manager = models.OneToOneField(BudgetManager, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"FamilyBudget(owner={self.budget_manager.user.email!r}, title={self.title!r})"
