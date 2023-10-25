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
    "id": int,
    "name": str,
    "number": str,
    "status": str,
    "geom": str,
}
DEPARTMENT_DATA_SERIALIZER_SCHEMA = {
    "name": str,
    "year": int,
    "download_link": str,
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
                "id": self.code_dor.id,
                "name": "Ain",
                "number": "01",
                "status": "not_available",
                "geom": str(self.code_dor.geom),
            },
        )


class DepartmentDownloadApiTestCase(APITestCase):
    def setUp(self):
        code_dor = DepartmentFactory(name="Côte d'Or", number="21")
        finistere = DepartmentFactory(name="Finistère", number="29")
        manche = DepartmentFactory(name="Manche", number="50")

        DepartmentDataFactory(
            department=code_dor, year=2008, download_link="http://rigo.lo"
        )
        DepartmentDataFactory(department=finistere)
        DepartmentDataFactory(department=manche)

    def test_get_data_departments(self):
        response = self.client.get("/api/department_data/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

        first_element = data[0]
        self.assertTrue(
            check_structure(first_element, DEPARTMENT_DATA_SERIALIZER_SCHEMA)
        )

        self.assertEquals(
            first_element,
            {
                "name": "21 - Côte d'Or - 2008",
                "year": 2008,
                "download_link": "http://rigo.lo",
            },
        )


class DepartmentDownloadDataApiTestCase(APITestCase):
    def setUp(self):
        self.department_data = DepartmentDataFactory()

    def test_get_data_departments(self):
        data = {
            "department_data": f"{self.department_data.id}",
            "username": "Michel",
            "organisation": "IGN",
            "email": "michel@allez.fcl",
        }
        response = self.client.post(
            "/api/department_data_downloads/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DepartmentDataDownload.objects.count(), 1)

        dep_data_download = DepartmentDataDownload.objects.first()

        self.assertEquals(dep_data_download.username, "Michel")
        self.assertEquals(dep_data_download.organisation, "IGN")
        self.assertEquals(dep_data_download.email, "michel@allez.fcl")
        self.assertEquals(dep_data_download.department_data, self.department_data)
