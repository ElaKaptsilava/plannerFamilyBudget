from django.db import models


class Plan(models.Model):
    name = models.CharField(
        max_length=120, unique=True, help_text="Enter name of the plan."
    )
    description = models.TextField(help_text="Enter description of the plan.")
    price = models.FloatField(help_text="Enter price of the plan.")

    def __str__(self) -> str:
        return f"{self.name} - ${self.price}"

    def __repr__(self) -> str:
        return str(self.name)
