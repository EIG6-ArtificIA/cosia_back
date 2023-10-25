from django.test import TestCase
from predictions_map.utils import check_structure


class UtilsTestCase(TestCase):
    def test_simple_cases(self):
        schema = {"foo": [{"bar": int}]}

        case = {"foo": [{"bar": 3}]}
        self.assertTrue(check_structure(case, schema))

        case = {"foo": [{"bar": "coucou"}]}
        self.assertFalse(check_structure(case, schema))

    def test_department_cases(self):
        schema = {"name": str, "number": str, "status": str, "geom": str}

        case = {
            "number": "0",
            "name": "Yonne",
            "status": "not_available",
            "geom": "SRID=2154;MULTIPOLYGON (((0 0, 0 1, 1 1, 0 0)), ((1 1, 1 2, 2 2, 1 1)))",
        }
        self.assertTrue(check_structure(case, schema))

        case = {
            "number": 0,
            "name": "Yonne",
            "status": "not_available",
            "geom": "SRID=2154;MULTIPOLYGON (((0 0, 0 1, 1 1, 0 0)), ((1 1, 1 2, 2 2, 1 1)))",
        }
        self.assertFalse(check_structure(case, schema))
