from minio.error import S3Error
from io import StringIO
from typing import Union, List
import os
import sys
from src.logger import logging
from pandas import DataFrame, read_csv
import pickle
from src.exception import MyException
from minio import Minio


class SimpleStorageService:
    """
    A class for interacting with MinIO storage, providing methods for file management, 
    data uploads, and data retrieval in MinIO buckets.
    """

    def __init__(self):
        """
        Initializes the SimpleStorageService instance with MinIO client 
        from the MinioClient class.
        """
        self.minio_client = Minio(
            endpoint="your-minio-endpoint",
            access_key="your-access-key",
            secret_key="your-secret-key",
            secure=False
        )

    def bucket_exists(self, bucket_name: str) -> bool:
        """
        Checks if the specified MinIO bucket exists.

        Args:
            bucket_name (str): The name of the MinIO bucket.

        Returns:
            bool: True if the bucket exists, False otherwise.
        """
        try:
            return self.minio_client.bucket_exists(bucket_name)
        except S3Error as e:
            raise MyException(e, sys)

    def read_object(self, bucket_name: str, object_name: str) -> Union[StringIO, str]:
        """
        Reads the specified MinIO object and returns its content.

        Args:
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object to read.

        Returns:
            Union[StringIO, str]: The content of the object as a StringIO or a string.
        """
        try:
            data = self.minio_client.get_object(bucket_name, object_name)
            content = data.read().decode('utf-8')
            return StringIO(content)
        except S3Error as e:
            raise MyException(e, sys)

    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str):
        """
        Uploads a local file to the specified MinIO bucket.

        Args:
            from_filename (str): Path of the local file.
            to_filename (str): Target file path in the bucket.
            bucket_name (str): Name of the MinIO bucket.
        """
    
        try:
            self.minio_client.fput_object(bucket_name, to_filename, from_filename)
            logging.info(f"File {from_filename} uploaded to {bucket_name}/{to_filename}")
        except S3Error as e:
            logging.error(f"Error uploading file {from_filename} to {bucket_name}/{to_filename}: {e}")
            raise MyException(e, sys)

       

    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str):
        """
        Uploads a DataFrame as a CSV file to the specified MinIO bucket.

        Args:
            data_frame (DataFrame): DataFrame to be uploaded.
            local_filename (str): Temporary local filename for the DataFrame.
            bucket_filename (str): Target filename in the bucket.
            bucket_name (str): Name of the MinIO bucket.
        """
        try:
            data_frame.to_csv(local_filename, index=None, header=True)
            self.upload_file(local_filename, bucket_filename, bucket_name)
        except Exception as e:
            raise MyException(e, sys)

    def load_model(self, model_name: str, bucket_name: str) -> object:
        """
        Loads a serialized model from the specified MinIO bucket.

        Args:
            model_name (str): Name of the model file in the bucket.
            bucket_name (str): Name of the MinIO bucket.

        Returns:
            object: The deserialized model object.
        """
        try:
            model_obj = self.read_object(bucket_name, model_name)
            model = pickle.loads(model_obj.getvalue())
            return model
        except Exception as e:
            raise MyException(e, sys)

    def get_df_from_object(self, bucket_name: str, object_name: str) -> DataFrame:
        """
        Converts a MinIO object to a DataFrame.

        Args:
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object.

        Returns:
            DataFrame: DataFrame created from the object content.
        """
        content = self.read_object(bucket_name, object_name)
        df = read_csv(content)
        return df
