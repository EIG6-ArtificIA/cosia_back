from boto3 import client
import wget
from progressbar.progressbar import ProgressBar
import os

from predictions_map.models import DepartmentData

# TODO move  into env var
S3_HOST = os.getenv("S3_HOST")
S3_REGION_NAME = os.getenv("S3_REGION_NAME")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")


class S3Client:
    @classmethod
    def getS3Client(cls):
        print("Chek !")
        print(S3_ACCESS_KEY_ID)
        print(S3_SECRET_ACCESS_KEY)
        print(S3_HOST)
        print(S3_REGION_NAME)
        print(S3_BUCKET)
        return client(
            endpoint_url=S3_HOST,
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY,
            service_name="s3",
            region_name=S3_REGION_NAME,
        )

    @classmethod
    def getAllObjectsInBucket(cls):
        client = cls.getS3Client()
        response = client.list_objects(Bucket=S3_BUCKET)
        return response["Contents"]

    @classmethod
    def printFormatedAllObjectsInBucket(cls):
        contents = cls.getAllObjectsInBucket()
        for obj in contents:
            size = "{:,}".format(obj["Size"])
            print(f"{obj['Key']} - Size : {size}")


class S3Upload:
    def __init__(self):
        self.s3 = S3Client.getS3Client()

    def upload_callback(self, size):
        self.pg.update(self.pg.currval + size)

    def upload(self, file, bucket, key):
        self.pg = ProgressBar(maxval=os.stat(file).st_size)
        self.pg.start()

        with open(file, "rb") as data:
            self.s3.upload_fileobj(data, bucket, key, Callback=self.upload_callback)


def clean(file_path):
    os.remove(file_path)


def __run__():
    s3Upload = S3Upload()

    for departmentData in DepartmentData.objects.all():
        print(f"--- {departmentData} ---")

        zip_file_path = wget.download(departmentData.download_link, "tmp")

        dep_number_with_3_characters = departmentData.department.number.zfill(3)
        s3_object_name = (
            f"CoSIA_D{dep_number_with_3_characters}_{departmentData.year}.zip"
        )
        s3Upload.upload(zip_file_path, S3_BUCKET, s3_object_name)

        departmentData.s3_object_name = s3_object_name
        departmentData.full_clean()
        departmentData.save()

        clean(zip_file_path)
        print(f"\nDone for {departmentData} !")
