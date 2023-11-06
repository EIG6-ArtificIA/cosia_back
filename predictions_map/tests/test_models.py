from django.core.exceptions import ValidationError
from django.test import TestCase
from predictions_map.models import Department, DepartmentData, DepartmentDataDownload
from predictions_map.tests.factories import (
    DepartmentDataFactory,
    DepartmentFactory,
    DepartmentDataDownloadFactory,
    MULTI_POLYGON,
)


class DepartmentTestCase(TestCase):
    def setUp(self):
        DepartmentFactory(name="Finistère", number=29, status=Department.SOON_AVAILABLE)
        DepartmentFactory(name="Côte d'Or", number="21")

    def test_departements_are_correctly_created(self):
        departments_count = Department.objects.count()

        self.assertEqual(departments_count, 2)

        finistere = Department.objects.get(number="29")

        self.assertEqual(finistere.name, "Finistère")
        self.assertEqual(finistere.number, "29")
        self.assertEqual(finistere.status, Department.SOON_AVAILABLE)
        self.assertEqual(finistere.geom, MULTI_POLYGON)

    def test_departement_default_status_is_not_available(self):
        cote_d_or = Department.objects.get(number="21")
        self.assertEqual(cote_d_or.status, Department.NOT_AVAILABLE)


class DepartmentDataTestCase(TestCase):
    def setUp(self):
        yonne = DepartmentFactory(name="Yonne", number="89")
        DepartmentDataFactory(department=yonne)
        DepartmentDataFactory(department=yonne)

    def test_departements_data_are_correctly_created(self):
        departments_data_count = DepartmentData.objects.count()

        self.assertEqual(departments_data_count, 2)

        yonne = Department.objects.get(name="Yonne")
        yonne_2015_data = DepartmentData.objects.filter(department=yonne).first()

        self.assertEqual(yonne_2015_data.department, yonne)
        self.assertEqual(yonne_2015_data.department.name, "Yonne")
        self.assertEqual(yonne_2015_data.zip_size, "1.0 Go")
        self.assertEqual(yonne_2015_data.file_size, "8.4 Go")

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
        too_old = DepartmentDataFactory(year=1849)

        with self.assertRaises(ValidationError):
            too_old.full_clean()

        too_much_in_future = DepartmentDataFactory(year=2101)

        with self.assertRaises(ValidationError):
            too_much_in_future.full_clean()

        min_date = DepartmentDataFactory(year=1850)
        min_date.full_clean()

        max_date = DepartmentDataFactory(year=2100)
        max_date.full_clean()

    def test_download_link_validation(self):
        not_a_link = DepartmentDataFactory(download_link="http://coucou")

        with self.assertRaises(ValidationError):
            not_a_link.full_clean()

        http_link = DepartmentDataFactory(download_link="http://coucou.co")
        http_link.full_clean()

        https_link = DepartmentDataFactory(download_link="https://coucou.fr")
        https_link.full_clean()

    def test_str_property(self):
        yonne = Department.objects.get(name="Yonne")
        yonne_data = DepartmentDataFactory(department=yonne, year=2000)

        self.assertEqual(yonne_data.__str__(), "89 - Yonne - 2000")


class DepartmentDataDownloadTestCase(TestCase):
    def setUp(self):
        DepartmentDataDownloadFactory()
        DepartmentDataDownloadFactory()

    def test_departements_data_download_are_correctly_created(self):
        departments_data_count = DepartmentDataDownload.objects.count()

        self.assertEqual(departments_data_count, 2)
