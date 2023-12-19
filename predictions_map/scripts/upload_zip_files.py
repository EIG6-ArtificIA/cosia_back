import os
from predictions_map.s3_client import S3Client, S3Upload
from os import listdir

FILES_DIR_PATH = "tmp/cosia_upload"


def upload_zip_files(env):
    s3_client = get_s3_client_from_env(env)
    s3_upload = S3Upload(s3_client)

    print(f"C'est parti pour le téléversement sur {env} !")

    files_list = listdir(FILES_DIR_PATH)
    all_objects_name = s3_client.get_all_objects_name_in_bucket()
    s3_client.print_formated_all_objects_in_bucket()

    for file_name in files_list:
        print(file_name, end="\n\n")
        file_already_in_s3 = file_name in all_objects_name

        if file_already_in_s3:
            overwrite_file = input(
                f"Le fichier {file_name} existe déjà sur le S3.\nVeux-tu l'écraser ? (oui/non)"
            )
            while overwrite_file not in ["oui", "non"]:
                overwrite_file = input(f"Je n'ai pas compris. oui ou non ?")

            if overwrite_file == "non":
                continue

        s3_upload.upload(f"{FILES_DIR_PATH}/{file_name}", file_name)

    print(f"C'est fait !")


def get_s3_client_from_env(env):
    if env not in ["prd", "qlf", "dev"]:
        raise ValueError(f"{env} n'est pas disponible. Choisir parmi prd, qlf et dev.")

    if env == "prd":
        return S3Client(
            s3_access_key_id=os.getenv("S3_ACCESS_KEY_ID_PRD"),
            s3_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY_PRD"),
            s3_bucket=os.getenv("S3_BUCKET_PRD"),
        )

    if env == "qlf":
        return S3Client(
            s3_access_key_id=os.getenv("S3_ACCESS_KEY_ID_QLF"),
            s3_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY_QLF"),
            s3_bucket=os.getenv("S3_BUCKET_QLF"),
        )

    return S3Client()
