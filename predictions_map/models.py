from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Department(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    geom = models.MultiPolygonField(srid=2154)
    number = models.IntegerField(
        unique=True, validators=[MinValueValidator(1), MaxValueValidator(976)]
    )
    status = models.CharField(max_length=100, null=False, blank=False)


class DepartmentData(models.Model):
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    download_link = models.CharField(max_length=300)
    year = models.IntegerField(
        validators=[MinValueValidator(1850), MaxValueValidator(2100)]
    )


class DepartmentDataDownload(models.Model):
    department_data = models.ForeignKey("DepartmentData", on_delete=models.CASCADE)
    username = models.CharField(max_length=120, null=False, blank=False)
    organisation = models.CharField(max_length=300, null=False, blank=False)
    email = models.CharField(max_length=150, null=False, blank=False)
