from minio import Minio
import os
from src.constants import MINIO_ACCESS_KEY_ENV_KEY, MINIO_SECRET_KEY_ENV_KEY, MINIO_URL

class MinioClient:

    minio_client = None

    def __init__(self, endpoint=MINIO_URL):
        """ 
        This Class gets MinIO credentials from environment variables and creates 
        a connection with the MinIO server and raises an exception if environment variables are not set.
        """

        if MinioClient.minio_client is None:
            __access_key = os.getenv(MINIO_ACCESS_KEY_ENV_KEY)
            __secret_key = os.getenv(MINIO_SECRET_KEY_ENV_KEY)
            if __access_key is None:
                raise Exception(f"Environment variable: {MINIO_ACCESS_KEY_ENV_KEY} is not set.")
            if __secret_key is None:
                raise Exception(f"Environment variable: {MINIO_SECRET_KEY_ENV_KEY} is not set.")

            MinioClient.minio_client = Minio(endpoint, access_key=__access_key, secret_key=__secret_key, secure=False)

        self.minio_client = MinioClient.minio_client
