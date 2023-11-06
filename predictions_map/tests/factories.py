from factory import SubFactory, Sequence
from factory.django import DjangoModelFactory
from predictions_map.models import Department, DepartmentData, DepartmentDataDownload
from django.contrib.gis.geos import Polygon, MultiPolygon
from faker import Faker

fake = Faker()

MULTI_POLYGON = MultiPolygon(
    Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
    Polygon(((1, 1), (1, 2), (2, 2), (1, 1))),
)


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = fake.random_element(
        elements=(
            "Côte d'Or",
            "Finistère",
            "Manche",
            "Morbihan",
            "Nord",
            "Yonne",
        )
    )
    number = Sequence(lambda n: f"{n}")
    geom = MULTI_POLYGON


class DepartmentDataFactory(DjangoModelFactory):
    class Meta:
        model = DepartmentData

    department = SubFactory(DepartmentFactory)
    download_link = fake.uri()
    year = fake.random_int(1850, 2100)
    file_size = "8.4 Go"
    zip_size = "1.0 Go"


class DepartmentDataDownloadFactory(DjangoModelFactory):
    class Meta:
        model = DepartmentDataDownload

    department_data = SubFactory(DepartmentDataFactory)
    username = fake.name()
    organization = fake.company()
    email = fake.email()
