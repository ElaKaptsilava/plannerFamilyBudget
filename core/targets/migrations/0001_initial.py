# Generated by Django 5.0.6 on 2024-08-06 11:51

import accounts.models.profile
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Saving",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        auto_now_add=True, help_text="Date of the saving entry."
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="saving",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SavingContributions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Enter the amount.",
                        max_digits=10,
                        verbose_name="Amount",
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        auto_now_add=True, help_text="Date of the contribution entry."
                    ),
                ),
                (
                    "saving",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="targets.saving",
                        verbose_name="Saving",
                    ),
                ),
            ],
            options={
                "ordering": ("date",),
            },
        ),
        migrations.CreateModel(
            name="Target",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=accounts.models.profile.get_upload_path,
                    ),
                ),
                (
                    "target",
                    models.CharField(
                        help_text="A name of the target goal.", max_length=255
                    ),
                ),
                (
                    "amount",
                    models.FloatField(
                        help_text="The amount of money required to achieve the target."
                    ),
                ),
                (
                    "deadline",
                    models.DateField(
                        default=django.utils.timezone.now,
                        help_text="The deadline for achieving the target. Defaults to one year from now.",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="A description of the target.", null=True
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="targets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TargetContribution",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.FloatField(
                        help_text="The amount of money contributed towards the target."
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        auto_now_add=True,
                        help_text="The date when the contribution was made. Automatically set to the current date.",
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        help_text="The target this contribution is associated with.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="targets.target",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-date",),
                "indexes": [
                    models.Index(
                        fields=["user"], name="targets_tar_user_id_755e19_idx"
                    ),
                    models.Index(
                        fields=["amount"], name="targets_tar_amount_c61e46_idx"
                    ),
                    models.Index(fields=["date"], name="targets_tar_date_f2960f_idx"),
                ],
            },
        ),
    ]
