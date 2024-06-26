# Generated by Django 5.0.6 on 2024-05-24 17:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("runningCosts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="runningcost",
            name="payment_deadline",
            field=models.DateField(
                default=django.utils.timezone.now,
                help_text="The deadline for paying the running cost.",
            ),
        ),
    ]
