# Generated by Django 4.1.6 on 2023-10-11 18:27

import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("predictions_map", "0005_rename_predictedarea_territory"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
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
                ("name", models.CharField(max_length=200)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=2154),
                ),
                (
                    "number",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(976),
                        ]
                    ),
                ),
                ("status", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="DepartmentData",
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
                ("download_link", models.CharField(max_length=300)),
                (
                    "year",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1850),
                            django.core.validators.MaxValueValidator(2100),
                        ]
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="predictions_map.department",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DepartmentDataDownload",
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
                ("username", models.CharField(max_length=120)),
                ("organisation", models.CharField(max_length=300)),
                ("email", models.CharField(max_length=150)),
                (
                    "department_data",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="predictions_map.departmentdata",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Territory",
        ),
    ]
