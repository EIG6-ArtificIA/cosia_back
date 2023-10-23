from django.test import TestCase
from predictions_map.models import Department, DepartmentData
from django.contrib.gis.geos import Polygon, MultiPolygon

MULTI_POLYGON = MultiPolygon(
    Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
    Polygon(((1, 1), (1, 2), (2, 2), (1, 1))),
)


class DepartmentTestCase(TestCase):
    def setUp(self):
        Department.objects.create(
            name="Finistère",
            number="29",
            geom=MULTI_POLYGON,
            status=Department.SOON_AVAILABLE,
        )
        Department.objects.create(name="Côte d'Or", number="21", geom=MULTI_POLYGON)

    def test_departements_are_correctly_created(self):
        departments_count = Department.objects.count()

        self.assertEqual(departments_count, 2)

        finistere = Department.objects.get(number="29")

        self.assertEqual(finistere.name, "Finistère")
        self.assertEqual(finistere.number, "29")
        self.assertEqual(finistere.status, Department.SOON_AVAILABLE)
        self.assertEqual(finistere.geom, MULTI_POLYGON)

    def test_departement_default_status_is_not_available(self):
        finistere = Department.objects.get(number="21")
        self.assertEqual(finistere.status, Department.NOT_AVAILABLE)


class DepartmentDataTestCase(TestCase):
    def setUp(self):
        yonne = Department.objects.create(name="Yonne", number="89", geom=MULTI_POLYGON)
        DepartmentData.objects.create(
            department=yonne, download_link="coucou", year=2015
        )
        DepartmentData.objects.create(
            department=yonne, download_link="coucou2", year=2018
        )

    def test_departements_data_are_correctly_created(self):
        departments_data_count = DepartmentData.objects.count()

        self.assertEqual(departments_data_count, 2)

        yonne = Department.objects.get(name="Yonne")
        yonne_2015_data = DepartmentData.objects.get(department=yonne, year=2015)

        self.assertEqual(yonne_2015_data.department, yonne)
        self.assertEqual(yonne_2015_data.department.name, "Yonne")
        self.assertEqual(yonne_2015_data.year, 2015)
        self.assertEqual(yonne_2015_data.download_link, "coucou")
