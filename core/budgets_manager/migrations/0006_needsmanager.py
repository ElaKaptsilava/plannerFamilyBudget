# Generated by Django 5.0.6 on 2024-06-16 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("budgets_manager", "0005_delete_needsmanager"),
    ]

    operations = [
        migrations.CreateModel(
            name="NeedsManager",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("budgets_manager.budgetmanager",),
        ),
    ]
