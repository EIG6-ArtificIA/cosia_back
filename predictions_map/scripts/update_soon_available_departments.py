from predictions_map.models import Department


SOON_AVAILABLE_DEPARTMENTS = [
    "22",
    "64",
    "24",
    "32",
    "47",
    "17",
    "66",
    "11",
    "34",
    "06",
    "04",
    "05",
    "84",
    "30",
    "48",
    "01",
    "68",
    "972",
    "59",
    "80",
    "02",
    "60",
    "75",
    "92",
    "93",
    "94",
    "78",
    "91",
    "37",
]


def update_soon_available_departments():
    print("Clean old soon available departments")
    soon_available_departments = Department.objects.filter(
        status=Department.SOON_AVAILABLE
    )
    soon_available_departments.update(status=Department.NOT_AVAILABLE)

    print("Update soon available departments")
    soon_available_departments = Department.objects.filter(
        number__in=SOON_AVAILABLE_DEPARTMENTS
    )
    soon_available_departments.update(status=Department.SOON_AVAILABLE)
    print("Tout est bon, allez la suite !")
