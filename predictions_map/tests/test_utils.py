from django.test import TestCase
from predictions_map.utils import check_structure, format_file_size


class CheckStructureTestCase(TestCase):
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


class FormatFileSizeTestCase(TestCase):
    def test_format_file_size(self):
        value_and_expected_value_list = [
            (500, "500 o"),
            (1_000, "1,0 Ko"),
            (500_000, "488,3 Ko"),
            (1_000_000, "976,6 Ko"),
            (75_405_000, "71,9 Mo"),
            (1_254_405_000, "1,2 Go"),
        ]

        for tuple in value_and_expected_value_list:
            (value, expected_value) = tuple
            self.assertEqual(format_file_size(value), expected_value)
