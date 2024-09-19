# Generated by Django 5.0.6 on 2024-09-19 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budgets_manager", "0006_monthlyincomes_total_income"),
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="budget",
            field=models.ForeignKey(
                default=10,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="expenses",
                to="budgets_manager.budgetmanager",
            ),
            preserve_default=False,
        ),
    ]
