from urllib.error import HTTPError
import wget
import os

from predictions_map.models import DepartmentData
from predictions_map.s3_client import S3Upload
from predictions_map.utils import get_formatted_file_size


def clean(file_path):
    os.remove(file_path)


def __run__():
    s3Upload = S3Upload()

    for departmentData in DepartmentData.objects.all():
        print(f"--- {departmentData} ---")
        try:
            zip_file_path = wget.download(departmentData.download_link, "tmp")

            dep_number_with_3_characters = departmentData.department.number.zfill(3)
            s3_object_name = (
                f"CoSIA_D{dep_number_with_3_characters}_{departmentData.year}.zip"
            )
            s3Upload.upload(zip_file_path, s3_object_name)

            zip_size = get_formatted_file_size(zip_file_path)
            departmentData.s3_object_name = s3_object_name
            departmentData.zip_size = zip_size
            departmentData.full_clean()
            departmentData.save()

            clean(zip_file_path)
            print(f"\nDone for {departmentData} !")
        except HTTPError as e:
            print(e)
