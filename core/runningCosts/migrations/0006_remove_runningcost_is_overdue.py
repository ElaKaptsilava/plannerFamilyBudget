# Generated by Django 5.0.6 on 2024-05-30 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("runningCosts", "0005_remove_runningcost_payment_day_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="runningcost",
            name="is_overdue",
        ),
    ]
