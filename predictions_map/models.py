from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Department(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    geom = models.MultiPolygonField(srid=2154)
    number = models.CharField(unique=True, max_length=3)
    status = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.number + " - " + self.name

    class Meta:
        ordering = ["number"]


class DepartmentData(models.Model):
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    download_link = models.CharField(max_length=300)
    year = models.IntegerField(
        validators=[MinValueValidator(1850), MaxValueValidator(2100)]
    )

    def __str__(self):
        return (
            self.department.number
            + " - "
            + self.department.name
            + " - "
            + str(self.year)
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print("Hollande")
        print(args)
        print(kwargs)


class DepartmentDataDownload(models.Model):
    department_data = models.ForeignKey("DepartmentData", on_delete=models.CASCADE)
    username = models.CharField(max_length=120, null=False, blank=False)
    organisation = models.CharField(max_length=300, null=False, blank=False)
    email = models.CharField(max_length=150, null=False, blank=False)
