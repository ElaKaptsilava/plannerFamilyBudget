# Generated by Django 5.0.6 on 2024-09-19 09:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budgets_manager", "0005_alter_setbudget_user"),
        ("incomes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="income",
            name="budget",
            field=models.ForeignKey(
                default=10,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="incomes",
                to="budgets_manager.budgetmanager",
            ),
            preserve_default=False,
        ),
    ]