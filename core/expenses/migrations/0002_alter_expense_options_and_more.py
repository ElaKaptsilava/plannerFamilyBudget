# Generated by Django 5.0.6 on 2024-05-23 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="expense",
            options={"ordering": ["-datetime"]},
        ),
        migrations.RenameField(
            model_name="expense",
            old_name="datatime",
            new_name="datetime",
        ),
    ]