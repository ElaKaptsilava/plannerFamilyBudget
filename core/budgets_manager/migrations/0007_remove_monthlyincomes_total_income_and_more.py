# Generated by Django 5.0.6 on 2024-06-26 17:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budgets_manager", "0006_alter_monthlyincomes_options_and_more"),
        ("expenses", "0001_initial"),
        ("runningCosts", "0002_alter_runningcost_period_type"),
        ("targets", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="monthlyincomes",
            name="total_income",
        ),
        migrations.AddConstraint(
            model_name="limitmanager",
            constraint=models.UniqueConstraint(
                fields=("user", "category_running_cost"),
                name="unique_user_category_running_cost",
            ),
        ),
        migrations.AddConstraint(
            model_name="limitmanager",
            constraint=models.UniqueConstraint(
                fields=("user", "category_expense"), name="unique_user_category_expense"
            ),
        ),
        migrations.AddConstraint(
            model_name="limitmanager",
            constraint=models.UniqueConstraint(
                fields=("user", "target"), name="unique_user_target"
            ),
        ),
    ]
