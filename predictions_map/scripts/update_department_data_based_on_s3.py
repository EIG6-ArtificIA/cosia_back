from predictions_map.s3_client import S3Client
from predictions_map.models import Department, DepartmentData
from predictions_map.s3_client import S3Client


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

            department_data = DepartmentData.objects.get(
                department=department, year=year
            )
            department_data.zip_size = zip_size
            department_data.save()

        Department = department

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
