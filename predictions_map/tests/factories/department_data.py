from factory.django import DjangoModelFactory
from predictions_map.models import Department
from django.contrib.gis.geos import Polygon, MultiPolygon

MULTI_POLYGON = MultiPolygon(
    Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
    Polygon(((1, 1), (1, 2), (2, 2), (1, 1))),
)


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = "Finistère"
    number = "29"
    geom = MULTI_POLYGON
