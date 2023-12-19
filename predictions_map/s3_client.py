from boto3 import client
from progressbar.progressbar import ProgressBar
import os

from predictions_map.utils import format_file_size


S3_HOST = os.getenv("S3_HOST")
S3_REGION_NAME = os.getenv("S3_REGION_NAME")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")


class S3Client:
    def __init__(
        self,
        s3_access_key_id=S3_ACCESS_KEY_ID,
        s3_secret_access_key=S3_SECRET_ACCESS_KEY,
        s3_bucket=S3_BUCKET,
    ):
        self.client = client(
            endpoint_url=S3_HOST,
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_secret_access_key,
            service_name="s3",
            region_name=S3_REGION_NAME,
        )
        self.bucket = s3_bucket

    def get_all_objects_in_bucket(self):
        response = self.client.list_objects(Bucket=self.bucket)
        return response["Contents"]

    def print_formated_all_objects_in_bucket(self):
        contents = self.get_all_objects_in_bucket()
        for obj in contents:
            size = format_file_size(obj["Size"])
            print(f"{obj['Key']} - Size : {size}")

    def get_all_objects_name_in_bucket(self):
        contents = self.get_all_objects_in_bucket()
        return list(map(lambda x: x["Key"], contents))

    def get_object_download_url(self, key):
        oneHour = 3600
        return self.client.generate_presigned_url(
            "get_object", Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=oneHour
        )


class S3Upload:
    def __init__(self, s3_client: S3Client):
        self.s3 = s3_client

    def upload_callback(self, size):
        self.pg.update(self.pg.currval + size)

    def upload(self, file, key):
        self.pg = ProgressBar(maxval=os.stat(file).st_size)
        self.pg.start()

        with open(file, "rb") as data:
            self.s3.client.upload_fileobj(
                data, self.s3.bucket, key, Callback=self.upload_callback
            )
