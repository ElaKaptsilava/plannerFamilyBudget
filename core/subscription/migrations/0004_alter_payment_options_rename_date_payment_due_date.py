# Generated by Django 5.0.6 on 2024-07-27 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("subscription", "0003_alter_payment_date"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="payment",
            options={"ordering": ["-due_date"]},
        ),
        migrations.RenameField(
            model_name="payment",
            old_name="date",
            new_name="due_date",
        ),
    ]