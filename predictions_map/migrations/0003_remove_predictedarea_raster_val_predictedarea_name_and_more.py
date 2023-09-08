# Generated by Django 4.1.6 on 2023-08-28 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions_map', '0002_rename_predictionsmap_predictedarea'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predictedarea',
            name='raster_val',
        ),
        migrations.AddField(
            model_name='predictedarea',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='predictedarea',
            name='status',
            field=models.CharField(default='', max_length=100),
        ),
    ]