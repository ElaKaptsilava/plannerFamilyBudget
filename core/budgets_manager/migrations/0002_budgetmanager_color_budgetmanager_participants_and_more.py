# Generated by Django 5.0.6 on 2024-09-17 13:32

import colorfield.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budgets_manager", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="budgetmanager",
            name="color",
            field=colorfield.fields.ColorField(
                default="#FF0000", image_field=None, max_length=25, samples=None
            ),
        ),
        migrations.AddField(
            model_name="budgetmanager",
            name="participants",
            field=models.ManyToManyField(
                default=list, related_name="participants", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="budgetmanager",
            name="title",
            field=models.CharField(default="Family", max_length=50),
        ),
    ]