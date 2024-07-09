# Generated by Django 5.0.6 on 2024-06-27 15:57

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budgets_manager", "0007_remove_monthlyincomes_total_income_and_more"),
        ("expenses", "0001_initial"),
        ("runningCosts", "0002_alter_runningcost_period_type"),
        ("targets", "0001_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="limitmanager",
            name="unique_user_category_running_cost",
        ),
        migrations.RemoveConstraint(
            model_name="limitmanager",
            name="unique_user_category_expense",
        ),
        migrations.RemoveConstraint(
            model_name="limitmanager",
            name="unique_user_target",
        ),
        migrations.RemoveField(
            model_name="limitmanager",
            name="user",
        ),
        migrations.AlterField(
            model_name="limitmanager",
            name="category_expense",
            field=models.ForeignKey(
                blank=True,
                help_text="Expense category for 'needs' type budget.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="expenses.expensecategory",
            ),
        ),
        migrations.AlterField(
            model_name="limitmanager",
            name="category_running_cost",
            field=models.ForeignKey(
                blank=True,
                help_text="Running cost category for 'needs' type budget.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="runningCosts.runningcostcategory",
            ),
        ),
        migrations.AlterField(
            model_name="limitmanager",
            name="target",
            field=models.ForeignKey(
                blank=True,
                help_text="Target category for 'wants' type budget.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="targets.target",
            ),
        ),
        migrations.AlterField(
            model_name="monthlyincomes",
            name="year",
            field=models.IntegerField(
                blank=True,
                help_text="Enter Year",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1900),
                    django.core.validators.MaxValueValidator(2124),
                ],
            ),
        ),
        migrations.AddConstraint(
            model_name="limitmanager",
            constraint=models.UniqueConstraint(
                fields=("budget_manager", "category_running_cost"),
                name="unique_budget_category_running_cost",
            ),
        ),
        migrations.AddConstraint(
            model_name="limitmanager",
            constraint=models.UniqueConstraint(
                fields=("budget_manager", "category_expense"),
                name="unique_budget_category_expense",
            ),
        ),
        migrations.AddConstraint(
            model_name="limitmanager",
            constraint=models.UniqueConstraint(
                fields=("budget_manager", "target"), name="unique_budget_target"
            ),
        ),
    ]