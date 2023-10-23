from django.test import TestCase
from predictions_map.models import Department
from django.contrib.gis.geos import Polygon, MultiPolygon


class DepartmentTestCase(TestCase):
    MULTI_POLYGON = MultiPolygon(
        Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
        Polygon(((1, 1), (1, 2), (2, 2), (1, 1))),
    )

    def setUp(self):
        Department.objects.create(
            name="Finistère", number="29", geom=DepartmentTestCase.MULTI_POLYGON
        )
        Department.objects.create(
            name="Côte d'Or", number="21", geom=DepartmentTestCase.MULTI_POLYGON
        )

    def test_departements_are_correctly_created(self):
        departments_count = Department.objects.count()

        self.assertEqual(departments_count, 2)

        finistere = Department.objects.get(number="29")

        self.assertEqual(finistere.name, "Finistère")
        self.assertEqual(finistere.number, "29")
        self.assertEqual(finistere.status, Department.NOT_AVAILABLE)
        self.assertEqual(finistere.geom, DepartmentTestCase.MULTI_POLYGON)
