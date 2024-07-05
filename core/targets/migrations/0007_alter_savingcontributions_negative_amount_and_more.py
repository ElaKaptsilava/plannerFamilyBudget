# Generated by Django 5.0.6 on 2024-07-05 12:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("targets", "0006_alter_savingcontributions_negative_amount_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="savingcontributions",
            name="negative_amount",
            field=models.FloatField(
                blank=True,
                default=0,
                help_text="Amount of the negative amount.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(0)],
                verbose_name="Negative amount",
            ),
        ),
        migrations.AlterField(
            model_name="savingcontributions",
            name="positive_amount",
            field=models.FloatField(
                blank=True,
                default=0,
                help_text="Amount of the positive amount.",
                null=True,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Positive amount",
            ),
        ),
    ]
