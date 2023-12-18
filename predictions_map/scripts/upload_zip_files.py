import os
from subprocess import run
from smb.SMBHandler import SMBHandler
from predictions_map.models import Department, DepartmentData
from predictions_map.s3_client import S3Client, S3Upload
from predictions_map.utils import compute_s3_object_name, get_formatted_file_size
from os import listdir

departments_data_to_upload = [
    ("06", "2020", "11,5 Go"),
    ("11", "2021", "15,3 Go"),
    ("17", "2021", "14,2 Go"),
    ("37", "2021", "11,0 Go"),
    ("66", "2021", "10,7 Go"),
    ("75", "2021", "0,4 Go"),
    ("78", "2021", "4,5 Go"),
    ("84", "2021", "11,1 Go"),
    ("91", "2021", "2,9 Go"),
    ("92", "2021", "0,8 Go"),
    ("93", "2021", "1,0 Go"),
    ("94", "2021", "1,0 Go"),
]


def upload_zip_files(env):
    s3Upload = get_s3_upload_from_env(env)

    print(f"C'est parti pour le téléversement sur {env} !")

    files_list = listdir("tmp/cosia_upload")
    for file_name in files_list:
        print(file_name)
        all_objects_name = S3Client.get_all_objects_name_in_bucket()
        file_already_in_s3 = file_name in all_objects_name
        # With a prompt give the possibility to re-write
        if file_already_in_s3:
            continue

        s3Upload.upload(f"tmp/cosia_upload/{file_name}", file_name)


# TODO separer
def update_department_data_based_on_s3_bucket():
    objects_in_bucket = S3Client.get_all_objects_in_bucket()

    print(f"C'est parti pour la mise à jour de la base de données !")

    for s3_object in objects_in_bucket:
        try:
            (number, year, zip_size) = parse_s3_object(s3_object)
        except ValueError:
            pass

        # for tuple_department_data_number_and_year in departments_data:
        #     (number, year, file_size) = tuple_department_data_number_and_year
        #     print(f"--- {number} - {year} ---")

        department = Department.objects.get(number=number)
        is_department_data_already_exists = DepartmentData.objects.filter(
            department=department, year=year
        ).exists()

        if is_department_data_already_exists:
            replace_file = input(
                f"Le départment {number} a déjà des données associées au millésime {year}.\nVeux-tu mettre à jour le Department Data ?"
            )
            while replace_file not in ["oui", "non"]:
                replace_file = input(f"Je n'ai pas compris. oui ou non ?")

            if replace_file == "non":
                continue

            DepartmentData.objects.get(department=department, year=year)

    #     file_name = compute_s3_object_name(number, year)
    #     zip_file_path = f"tmp/{file_name}"
    #     cmd_to_execute = f"smbget smb://store/store-echange/EBookjans/CoSIA_proto/{file_name} -o {zip_file_path}"
    #     run(cmd_to_execute, shell=True, executable="/bin/bash")

    #     s3Upload.upload(zip_file_path, file_name)

    #     zip_size = get_formatted_file_size(zip_file_path)
    #     departmentData = DepartmentData(
    #         department=department,
    #         year=year,
    #         s3_object_name=file_name,
    #         zip_size=zip_size,
    #         file_size=file_size,
    #     )
    #     departmentData.full_clean()
    #     departmentData.save()


def get_s3_upload_from_env(env):
    if env not in ["prd", "qlf", "dev"]:
        raise ValueError(f"{env} n'est pas disponible. Choisir parmi prd, qlf et dev.")

    if env == "prd":
        return S3Upload(
            s3_host=os.getenv("S3_HOST_PRD"),
            s3_region_name=os.getenv("S3_REGION_NAME_PRD"),
            s3_access_key_id=os.getenv("S3_ACCESS_KEY_ID_PRD"),
            s3_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY_PRD"),
        )

    if env == "QLF":
        return S3Upload(
            s3_host=os.getenv("S3_HOST_QLF"),
            s3_region_name=os.getenv("S3_REGION_NAME_QLF"),
            s3_access_key_id=os.getenv("S3_ACCESS_KEY_ID_QLF"),
            s3_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY_QLF"),
        )

    return S3Upload()


def parse_s3_object(s3_object: str):
    s3_object_name = s3_object["Key"]
    splitted_name = s3_object_name.split("_")
    if len(splitted_name) != 3:
        raise ValueError(
            f"Nom de l'objet : {s3_object_name} => le script est fait pour mettre à jour la DB avec des objets au format CoSIA_DXXX_YYYY.zip"
        )

    year = splitted_name[-1].split(".")[0]

    department_number = splitted_name[1].strip("D")
    if department_number.startswith("0"):
        department_number = department_number[1:]

    zip_size = s3_object["Size"]

    return (department_number, year, zip_size)
