from urllib.error import HTTPError
import wget
import os
from django.db.models import Q


from predictions_map.models import DepartmentData
from predictions_map.s3_client import S3Upload
from predictions_map.utils import get_formatted_file_size


def clean(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f"File not found : {file_path}")


def compute_s3_object_name(departmentData):
    dep_number_with_3_characters = departmentData.department.number.zfill(3)
    return f"CoSIA_D{dep_number_with_3_characters}_{departmentData.year}.zip"


def migrate_zip_files(only_departments_without_s3_object_name=False):
    s3Upload = S3Upload()

    if only_departments_without_s3_object_name:
        selected_departement_data = DepartmentData.objects.filter(
            Q(s3_object_name__exact="")
        )
    else:
        selected_departement_data = DepartmentData.objects.all()

    for departmentData in selected_departement_data:
        print(f"--- {departmentData} ---")
        zip_file_path = ""

        try:
            zip_file_path = wget.download(departmentData.download_link, "tmp")

            s3_object_name = compute_s3_object_name(departmentData)
            s3Upload.upload(zip_file_path, s3_object_name)

            zip_size = get_formatted_file_size(zip_file_path)
            departmentData.s3_object_name = s3_object_name
            departmentData.zip_size = zip_size
            departmentData.full_clean()
            departmentData.save()

            print(f"\nDone for {departmentData} !")
        except HTTPError as e:
            print(e)
        finally:
            clean(zip_file_path)
