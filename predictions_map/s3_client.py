from boto3 import client
from progressbar.progressbar import ProgressBar
import os


S3_HOST = os.getenv("S3_HOST")
S3_REGION_NAME = os.getenv("S3_REGION_NAME")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")


class S3Client:
    @classmethod
    def getS3Client(cls):
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

    @classmethod
    def getObjectDownloadUrl(cls, key):
        s3Client = cls.getS3Client()
        oneHour = 3600
        return s3Client.generate_presigned_url(
            "get_object", Params={"Bucket": S3_BUCKET, "Key": key}, ExpiresIn=oneHour
        )


class S3Upload:
    def __init__(self):
        self.s3 = S3Client.getS3Client()

    def upload_callback(self, size):
        self.pg.update(self.pg.currval + size)

    def upload(self, file, key):
        self.pg = ProgressBar(maxval=os.stat(file).st_size)
        self.pg.start()

        with open(file, "rb") as data:
            self.s3.upload_fileobj(data, S3_BUCKET, key, Callback=self.upload_callback)
