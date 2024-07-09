# Generated by Django 5.0.6 on 2024-07-05 09:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("runningCosts", "0002_alter_runningcost_period_type"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="runningcost",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="running_costs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddIndex(
            model_name="runningcost",
            index=models.Index(fields=["user"], name="runningCost_user_id_f56fb9_idx"),
        ),
        migrations.AddIndex(
            model_name="runningcost",
            index=models.Index(
                fields=["next_payment_date"], name="runningCost_next_pa_2bec7b_idx"
            ),
        ),
    ]