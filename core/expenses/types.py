from django.db import models


class Type(models.TextChoices):
    WANTS = ("wants", "Wants")
    NEEDS = ("needs", "Needs")
