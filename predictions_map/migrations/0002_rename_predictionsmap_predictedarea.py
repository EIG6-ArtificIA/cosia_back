# Generated by Django 4.1.6 on 2023-02-08 16:16

from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ("predictions_map", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="PredictionsMap",
            new_name="PredictedArea",
        ),
    ]
