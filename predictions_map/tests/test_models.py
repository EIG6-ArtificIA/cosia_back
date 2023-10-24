from django.core.exceptions import ValidationError
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

    def test_departement_department_status_is_available(self):
        yonne_2015_data = DepartmentData.objects.first()
        yonne = yonne_2015_data.department

        self.assertEqual(yonne.status, Department.AVAILABLE)

    def test_departement_department_status_is_not_available_when_data_deleted(self):
        yonne = Department.objects.get(name="Yonne")
        yonne_data = yonne.data

        self.assertEqual(yonne_data.count(), 2)

        yonne_data.first().delete()
        yonne_data.last().delete()

        self.assertEqual(yonne_data.count(), 0)

        self.assertEqual(yonne.status, Department.NOT_AVAILABLE)

    def test_year_validation(self):
        yonne = Department.objects.get(name="Yonne")
        too_old = DepartmentData(
            department=yonne, download_link="http://rigo.lo", year=1849
        )

        with self.assertRaises(ValidationError):
            too_old.full_clean()

        too_much_in_future = DepartmentData(
            department=yonne, download_link="coucou", year=2101
        )

        with self.assertRaises(ValidationError):
            too_much_in_future.full_clean()

        min_date = DepartmentData(
            department=yonne, download_link="http://rigo.lo", year=1850
        )
        min_date.full_clean()
        max_date = DepartmentData(
            department=yonne, download_link="http://allez.co", year=2100
        )
        max_date.full_clean()

    def test_download_link_validation(self):
        yonne = Department.objects.get(name="Yonne")
        not_a_link = DepartmentData(
            department=yonne, download_link="http://coucou", year=2000
        )

        with self.assertRaises(ValidationError):
            not_a_link.full_clean()

        http_link = DepartmentData(
            department=yonne, download_link="http://coucou.co", year=2000
        )
        http_link.full_clean()

        https_link = DepartmentData(
            department=yonne, download_link="https://coucou.fr", year=2000
        )
        https_link.full_clean()

    def test_str_property(self):
        yonne = Department.objects.get(name="Yonne")
        yonne_data = DepartmentData(department=yonne, year=2000)

        self.assertEqual(yonne_data.__str__(), "89 - Yonne - 2000")
