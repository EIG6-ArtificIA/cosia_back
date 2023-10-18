# Generated by Django 4.1.6 on 2023-10-16 09:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("predictions_map", "0008_alter_department_number"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="department",
            options={"ordering": ["number"]},
        ),
        migrations.AlterField(
            model_name="department",
            name="status",
            field=models.CharField(
                choices=[
                    ("available", "Disponible"),
                    ("soon", "Bientôt disponible"),
                    ("not_available", "Pas disponible"),
                ],
                default="not_available",
                max_length=30,
            ),
        ),
    ]