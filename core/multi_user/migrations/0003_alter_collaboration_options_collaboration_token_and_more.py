# Generated by Django 5.0.6 on 2024-08-06 13:13

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("multi_user", "0002_remove_collaboration_users_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="collaboration",
            options={"ordering": ["user"]},
        ),
        migrations.AddField(
            model_name="collaboration",
            name="token",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                help_text="Unique token for user",
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="collaboration",
            name="user",
            field=models.OneToOneField(
                help_text="User to collaborate",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="invitation",
            name="token",
            field=models.CharField(help_text="Token", max_length=100),
        ),
    ]
