from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator


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

    class Meta:
        ordering = ["number"]


class DepartmentData(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    download_link = models.CharField(
        max_length=300, validators=[URLValidator(schemes=["http", "https"])]
    )
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
        self.department.status = Department.AVAILABLE
        self.department.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        dep = self.department
        if dep.data.count() == 0:
            self.department.status = Department.NOT_AVAILABLE
            self.department.save()


class DepartmentDataDownload(models.Model):
    department_data = models.ForeignKey("DepartmentData", on_delete=models.CASCADE)
    username = models.CharField(max_length=120, null=False, blank=False)
    organisation = models.CharField(max_length=300, null=False, blank=False)
    email = models.CharField(max_length=150, null=False, blank=False)
