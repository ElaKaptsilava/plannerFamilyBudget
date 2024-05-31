# Generated by Django 5.0.6 on 2024-05-31 13:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("runningCosts", "0006_remove_runningcost_is_overdue"),
    ]

    operations = [
        migrations.AlterField(
            model_name="runningcost",
            name="period",
            field=models.PositiveSmallIntegerField(
                help_text="The number of periods (e.g., 2 for bi-monthly).",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(12),
                ],
            ),
        ),
    ]
