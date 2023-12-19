# Generated by Django 4.1.6 on 2023-12-19 10:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("predictions_map", "0016_remove_departmentdata_download_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="departmentdata",
            name="file_size",
            field=models.CharField(
                blank=True,
                max_length=10,
                validators=[
                    django.core.validators.RegexValidator(
                        "^\\d{1,3},?\\d{0,1} [GM]o$",
                        "Veuillez entrer un texte de type 'XX,X Go' ou 'XXX,X Mo'",
                    )
                ],
            ),
        ),
    ]
