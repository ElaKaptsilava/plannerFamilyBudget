# Generated by Django 5.0.6 on 2024-09-17 10:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("multi_user", "0005_familybudget_color_familybudget_title"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="familybudget",
            name="members",
            field=models.ManyToManyField(
                default=list, related_name="family_budgets", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
