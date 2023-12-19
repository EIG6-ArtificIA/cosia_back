from predictions_map.s3_client import S3Client
from predictions_map.models import Department, DepartmentData
from predictions_map.utils import format_file_size


def update_department_data_based_on_s3_bucket(possibility_to_overwrite=False):
    s3_client = S3Client()
    objects_in_bucket = s3_client.get_all_objects_in_bucket()

    print(f"C'est parti pour la mise à jour de la base de données !")

    for s3_object in objects_in_bucket:
        parse_and_save(s3_object, possibility_to_overwrite)


def parse_and_save(s3_object, possibility_to_overwrite: bool):
    s3_object_name = s3_object["Key"]
    print(f"\n{s3_object_name}")
    try:
        (number, year, zip_size) = parse_s3_object(s3_object)
    except ValueError:
        print(
            f"Nom de l'objet : {s3_object_name} => le script est fait pour mettre à jour la DB avec des objets au format CoSIA_DXXX_YYYY.zip"
        )
        return

    department = Department.objects.get(number=number)
    is_department_data_already_exists = DepartmentData.objects.filter(
        department=department, year=year
    ).exists()

    if is_department_data_already_exists:
        if possibility_to_overwrite:
            overwrite_department_data(department, year, zip_size)
        else:
            print("On skip !")
        return

    department_data = DepartmentData(
        department=department,
        year=year,
        zip_size=zip_size,
        s3_object_name=s3_object_name,
    )
    department_data.full_clean()
    department_data.save()
    print("Sauvé !")


def parse_s3_object(s3_object: str):
    s3_object_name = s3_object["Key"]
    splitted_name = s3_object_name.split("_")
    if len(splitted_name) != 3 or splitted_name[0] != "CoSIA":
        raise ValueError(
            f"Nom de l'objet : {s3_object_name} => le script est fait pour mettre à jour la DB avec des objets au format CoSIA_DXXX_YYYY.zip"
        )

    year = splitted_name[-1].split(".")[0]

    department_number = splitted_name[1].strip("D")
    if department_number.startswith("0"):
        department_number = department_number[1:]

    zip_size = format_file_size(s3_object["Size"])

    return (department_number, int(year), zip_size)


def overwrite_department_data(department: Department, year: int, zip_size: int):
    replace_file = input(
        f"Le départment {department.number} a déjà des données associées au millésime {year}.\nVeux-tu mettre à jour le Department Data ?"
    )
    while replace_file not in ["oui", "non"]:
        replace_file = input(f"Je n'ai pas compris. oui ou non ?")

    if replace_file == "non":
        return

    department_data = DepartmentData.objects.get(department=department, year=year)
    department_data.zip_size = zip_size
    department_data.full_clean()
    department_data.save()
    print("Ecrasé !")
