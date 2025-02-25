import boto3

from settings.config import aws_secret_access_key, aws_access_key_id
from utils import logger


class S3Client:

    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name="ap-southeast-1",
        )

    def upload(self, file_content, bucket_name, file_name):
        try:
            self.client.upload_fileobj(file_content, bucket_name, file_name)
            return True
        except Exception as e:
            logger.exception(f"Error uploading resource. {type(e)}: {str(e)}")
            return False

    def create_presigned_url(self, key, bucket="iit-assay"):
        return s3_client.generate_presigned_url(
            ClientMethod="get_object", Params={"Bucket": bucket, "Key": key}
        )

    def upload_local_file(self, local_file_path, bucket_name, s3_key):
        try:
            s3_client.upload_file(local_file_path, bucket_name, s3_key)
            logger.info(f"File uploaded successfully to {bucket_name}/{s3_key}")
        except Exception as e:
            logger.exception(f"Error uploading file: {e}")


s3_client = S3Client()
