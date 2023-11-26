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


def upload_zip_files():
    print("C'est parti pour le téléversement !")
    s3Upload = S3Upload()
    files_list = listdir("tmp/cosia_upload")
    for file_name in files_list:
        print(file_name)
        all_objects_name = S3Client.get_all_objects_name_in_bucket()
        file_already_in_s3 = file_name in all_objects_name
        # With a prompt give the possibility of re-write
        if file_already_in_s3:
            continue

        s3Upload.upload(f"tmp/cosia_upload/{file_name}", file_name)

    # for tuple_department_data_number_and_year in departments_data:
    #     (number, year, file_size) = tuple_department_data_number_and_year
    #     print(f"--- {number} - {year} ---")

    #     department = Department.objects.get(number=number)
    #     is_department_data_already_exists = DepartmentData.objects.filter(
    #         department=department, year=year
    #     ).exists()

    #     if is_department_data_already_exists:
    #         replace_file = input(
    #             f"Le départment {number} a déjà des données associées au millésime {year}.\nVeux-tu téléverser le fichier zip et potentiellement remplacer le fichier déjà existant ? (oui/non)"
    #         )
    #         while replace_file not in ["oui", "non"]:
    #             replace_file = input(f"Je n'ai pas compris. oui ou non ?")

    #         if replace_file == "non":
    #             continue

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
