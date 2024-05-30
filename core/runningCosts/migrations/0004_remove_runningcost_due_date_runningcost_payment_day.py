# Generated by Django 5.0.6 on 2024-05-28 17:04

import runningCosts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("runningCosts", "0003_runningcost_is_paid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="runningcost",
            name="due_date",
        ),
        migrations.AddField(
            model_name="runningcost",
            name="payment_day",
            field=runningCosts.models.DayOfMonthField(
                default=15, help_text="The day of the month for payment."
            ),
        ),
    ]
