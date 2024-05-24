# Generated by Django 5.0.6 on 2024-05-24 16:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="RunningCostCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Enter the category of the running coast.",
                        max_length=256,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Enter the category description.",
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RunningCost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                (
                    "amount",
                    models.FloatField(
                        help_text="The amount of money for the running cost."
                    ),
                ),
                (
                    "period_type",
                    models.CharField(
                        choices=[
                            ("days", "Days"),
                            ("weeks", "Weeks"),
                            ("months", "Months"),
                            ("years", "Years"),
                        ],
                        default="months",
                        help_text="The type of period for the running cost (e.g., months, weeks).",
                        max_length=256,
                    ),
                ),
                (
                    "period",
                    models.PositiveSmallIntegerField(
                        help_text="The number of periods (e.g., 2 for bi-monthly)."
                    ),
                ),
                (
                    "due_date",
                    models.DateField(help_text="The due date for the next payment."),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="running_costs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="running_costs",
                        to="runningCosts.runningcostcategory",
                    ),
                ),
            ],
        ),
    ]
