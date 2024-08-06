from accounts.models import CustomUser
from budgets_manager.models import BudgetManager
from django.db import models


class Collaboration(models.Model):
    budget_manager = models.OneToOneField(BudgetManager, on_delete=models.CASCADE)
    users = models.ManyToManyField(
        CustomUser, related_name="collaborations", through="CollaborationUser"
    )

    def __str__(self) -> str:
        return f"Collaboration for {self.budget_manager}"

    def __repr__(self) -> str:
        return f"Collaboration for {self.budget_manager}"


class CollaborationUser(models.Model):
    collaboration = models.OneToOneField(Collaboration, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.collaboration} - {self.user}"

    def __repr__(self) -> str:
        return f"{self.collaboration} - {self.user}"
