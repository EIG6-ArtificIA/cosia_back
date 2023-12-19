from django.contrib.gis.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)


class Department(models.Model):
    AVAILABLE = "available"
    SOON_AVAILABLE = "soon"
    NOT_AVAILABLE = "not_available"
    STATUS_CHOICES = [
        (AVAILABLE, "Disponible"),
        (SOON_AVAILABLE, "Bientôt disponible"),
        (NOT_AVAILABLE, "Pas disponible"),
    ]

    name = models.CharField(max_length=200, null=False, blank=False)
    geom = models.MultiPolygonField(srid=2154)
    number = models.CharField(unique=True, max_length=3)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=30,
        null=False,
        blank=False,
        default=NOT_AVAILABLE,
    )

    def __str__(self):
        return self.number + " - " + self.name

    @property
    def data(self):
        return self.departmentdata_set.all()

    @property
    def geom_geojson(self):
        return self.geom.geojson

    @property
    def centroid_geojson(self):
        return self.geom.centroid.geojson

    class Meta:
        ordering = ["number"]


class DepartmentData(models.Model):
    FILE_VALIDATOR = RegexValidator(
        r"^\d{1,3},?\d{0,1} [GM]o$",
        "Veuillez entrer un texte de type 'XX,X Go' ou 'XXX,X Mo'",
    )

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField(
        validators=[MinValueValidator(1850), MaxValueValidator(2100)]
    )
    file_size = models.CharField(max_length=10, validators=[FILE_VALIDATOR], blank=True)
    zip_size = models.CharField(max_length=10, validators=[FILE_VALIDATOR])
    s3_object_name = models.CharField(max_length=300, blank=True)

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
        self.department.status = Department.AVAILABLE
        self.department.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        dep = self.department
        if dep.data.count() == 0:
            dep.status = Department.NOT_AVAILABLE
            dep.save()

    class Meta:
        ordering = ["department__number"]


class DepartmentDataDownload(models.Model):
    department_data = models.ForeignKey("DepartmentData", on_delete=models.CASCADE)
    username = models.CharField(max_length=120, null=False, blank=False)
    organization = models.CharField(max_length=300, null=False, blank=False)
    email = models.CharField(max_length=150, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
