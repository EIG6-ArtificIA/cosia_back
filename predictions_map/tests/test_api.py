import json
from rest_framework import status
from rest_framework.test import APITestCase
from predictions_map.models import DepartmentDataDownload
from predictions_map.tests.factories import (
    DepartmentDataFactory,
    DepartmentFactory,
)
from predictions_map.utils import check_structure

DEPARTMENT_SERIALIZER_SCHEMA = {
    "name": str,
    "number": str,
    "status": str,
    "geom": str,
}
DEPARTMENT_DATA_SERIALIZER_SCHEMA = {
    "id": int,
    "year": int,
    "download_link": str,
    "department": {"number": str, "name": str},
    "file_size": str,
    "zip_size": str,
}


class DepartmentApiTestCase(APITestCase):
    def setUp(self):
        self.code_dor = DepartmentFactory(name="Ain", number="01")
        DepartmentFactory.create_batch(3)

    def test_get_departments(self):
        response = self.client.get("/api/departments/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 4)

        ain = list(filter(lambda dep: dep["name"] == "Ain", data))[0]
        self.assertTrue(check_structure(ain, DEPARTMENT_SERIALIZER_SCHEMA))

        self.assertEquals(
            ain,
            {
                "name": "Ain",
                "number": "01",
                "status": "not_available",
                "geom": str(self.code_dor.geom),
            },
        )


class DepartmentDataApiTestCase(APITestCase):
    def setUp(self):
        cote_dor = DepartmentFactory(name="Côte d'Or", number="21")
        finistere = DepartmentFactory(name="Finistère", number="29")
        manche = DepartmentFactory(name="Manche", number="50")

        self.cote_dor_data = DepartmentDataFactory(
            department=cote_dor, year=1850, download_link="http://rigo.lo"
        )
        DepartmentDataFactory(department=finistere)
        DepartmentDataFactory(department=manche)

    def test_get_data_departments(self):
        response = self.client.get("/api/department-data/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

        first_element = data[0]

        self.assertEquals(
            first_element,
            {
                "id": self.cote_dor_data.id,
                "department": {"number": "21", "name": "Côte d'Or"},
                "year": 1850,
                "download_link": "http://rigo.lo",
                "file_size": "8.4 Go",
                "zip_size": "1.0 Go",
            },
        )

        self.assertTrue(
            check_structure(first_element, DEPARTMENT_DATA_SERIALIZER_SCHEMA)
        )


class DepartmentDataDownloadApiTestCase(APITestCase):
    def setUp(self):
        self.department_data = DepartmentDataFactory()

    def test_get_data_departments(self):
        data = {
            "department_data": self.department_data.id,
            "username": "Michel",
            "organization": "IGN",
            "email": "michel@allez.fcl",
        }
        response = self.client.post(
            "/api/department-data-downloads/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DepartmentDataDownload.objects.count(), 1)

        dep_data_download = DepartmentDataDownload.objects.first()

        self.assertEquals(dep_data_download.username, "Michel")
        self.assertEquals(dep_data_download.organization, "IGN")
        self.assertEquals(dep_data_download.email, "michel@allez.fcl")
        self.assertEquals(dep_data_download.department_data, self.department_data)
