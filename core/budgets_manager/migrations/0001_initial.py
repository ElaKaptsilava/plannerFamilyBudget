# Generated by Django 5.0.6 on 2024-06-14 09:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("expenses", "0001_initial"),
        ("runningCosts", "0001_initial"),
        ("targets", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BudgetManager",
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
                    "savings_percentage",
                    models.DecimalField(
                        decimal_places=1,
                        help_text="Percentage of the income allocated for savings.",
                        max_digits=5,
                    ),
                ),
                (
                    "wants_percentage",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Percentage of the income allocated for wants.",
                        max_digits=5,
                    ),
                ),
                (
                    "needs_percentage",
                    models.DecimalField(
                        decimal_places=1,
                        help_text="Percentage of the income allocated for needs.",
                        max_digits=5,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        help_text="The user this budget is associated with.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Planner",
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
                    "type",
                    models.CharField(
                        choices=[("wants", "Wants"), ("needs", "Needs")],
                        help_text="Type of budget category.",
                        max_length=10,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Amount allocated to this budget entry.",
                        max_digits=20,
                    ),
                ),
                (
                    "budget_manager",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="budgets_manager.budgetmanager",
                    ),
                ),
                (
                    "category_expense",
                    models.OneToOneField(
                        blank=True,
                        help_text="Expense category for 'needs' type budget.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="expenses.expensecategory",
                    ),
                ),
                (
                    "category_running_cost",
                    models.OneToOneField(
                        blank=True,
                        help_text="Running cost category for 'needs' type budget.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="runningCosts.runningcostcategory",
                    ),
                ),
                (
                    "target",
                    models.OneToOneField(
                        blank=True,
                        help_text="Target category for 'wants' type budget.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="targets.target",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        help_text="The user this budget is associated with.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
