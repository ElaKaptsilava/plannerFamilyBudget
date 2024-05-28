# Generated by Django 5.0.6 on 2024-05-25 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("runningCosts", "0002_runningcost_payment_deadline"),
    ]

    operations = [
        migrations.AddField(
            model_name="runningcost",
            name="is_paid",
            field=models.BooleanField(
                default=False,
                help_text="Indicates whether the running cost has been paid or not.",
            ),
        ),
    ]