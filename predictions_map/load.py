from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from django.forms import ValidationError
from .models import Department, DepartmentData

predictionsmap_mapping = {"name": "NOM", "geom": "MULTIPOLYGON", "number": "INSEE_DEP"}

french_departments = (
    Path(__file__).resolve().parent / "data" / "french_metropolitan_departments.gpkg"
)


def department_load(verbose=True):
    lm = LayerMapping(
        Department, french_departments, predictionsmap_mapping, transform=False
    )
    lm.save(strict=True, verbose=verbose)


DEPARTMENT_DATA = [
    {
        "department_number": "29",
        "year": "2021",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D029_2021.zip",
        "zip_size": "3,0 Go",
        "size": "12 Go",
    },
    {
        "department_number": "33",
        "year": "2021",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D033_2021.zip",
        "zip_size": "5,0 Go",
        "size": "20 Go",
    },
    {
        "department_number": "35",
        "year": "2020",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D035_2020.zip",
        "zip_size": "3,1 Go",
        "size": "12 Go",
    },
    {
        "department_number": "38",
        "year": "2021",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D038_2021.zip",
        "zip_size": "3,8 Go",
        "size": "15 Go",
    },
    {
        "department_number": "40",
        "year": "2021",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D040_2021.zip",
        "zip_size": "4,7 Go",
        "size": "19 Go",
    },
    {
        "department_number": "44",
        "year": "2022",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D044_2022.zip",
        "zip_size": "3,6 Go",
        "size": "15 Go",
    },
    {
        "department_number": "62",
        "year": "2021",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D062_2021.zip",
        "zip_size": "2,1 Go",
        "size": "8,6 Go",
    },
    {
        "department_number": "67",
        "year": "2021",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D067_2021.zip",
        "zip_size": "1,8 Go",
        "size": "7,3 Go",
    },
    {
        "department_number": "69",
        "year": "2020",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D069_2020.zip",
        "zip_size": "1,5 Go",
        "size": "6,0 Go",
    },
    {
        "department_number": "77",
        "year": "2021",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D077_2021.zip",
        "zip_size": "1,7 Go",
        "size": "7,8 Go",
    },
    {
        "department_number": "83",
        "year": "2020",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D083_2020.zip",
        "zip_size": "4,2 Go",
        "size": "18 Go",
    },
    {
        "department_number": "95",
        "year": "2021",
        "link": "https://filedn.eu/lMasUDxMj4Mfo9XOassyn4b/CoSIA_D095_2021.zip",
        "zip_size": "722,4 Mo",
        "size": "2,8 Go",
    },
]


def department_data_load():
    print("--- department data loading ---")
    for dd in DEPARTMENT_DATA:
        dep = Department.objects.get(number=dd.get("department_number"))
        print(dep)
        (dep_data, _) = DepartmentData.objects.get_or_create(
            department=dep,
            year=dd.get("year"),
        )
        dep_data.download_link = dd.get("link")
        dep_data.file_size = dd.get("size")
        dep_data.zip_size = dd.get("zip_size")
        try:
            dep_data.full_clean()
            dep_data.save()
            print("done !")

        except ValidationError as e:
            print("Error !")
            print(dd)
            print(e)
