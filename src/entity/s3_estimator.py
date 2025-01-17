from src.cloud_storage.minio_storage import SimpleStorageService
from src.exception import MyException
from src.entity.estimator import MyModel
import sys
from pandas import DataFrame

class Proj1Estimator:
    """
    This class is used to save and retrieve our model from MinIO bucket and to do prediction.
    """

    def __init__(self, bucket_name, model_path):
        """
        :param bucket_name: Name of your model bucket.
        :param model_path: Location of your model in bucket.
        """
        self.bucket_name = bucket_name
        self.minio_service = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: MyModel = None

    def is_model_present(self, model_path):
        """
        Check if the model is present in MinIO bucket.
        :param model_path: Path of the model in the bucket.
        :return: True if model exists, else False.
        """
        try:
            return self.minio_service.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
        except MyException as e:
            print(e)
            return False

    def load_model(self) -> MyModel:
        """
        Load the model from MinIO storage.
        :return: Loaded model.
        """
        try:
            return self.minio_service.load_model(self.model_path, bucket_name=self.bucket_name)
        except MyException as e:
            print(f"Error loading model: {e}")
            raise

    def save_model(self, from_file, remove: bool = False) -> None:
        """
        Save the model to MinIO storage.
        :param from_file: Local path of the model.
        :param remove: Whether to remove the local file after upload.
        :return: None
        """
        try:
            self.minio_service.upload_file(from_file,
                                           to_filename=self.model_path,
                                           bucket_name=self.bucket_name,
                                           remove=remove)
        except Exception as e:
            raise MyException(e, sys)

    def predict(self, dataframe: DataFrame):
        """
        Perform prediction using the loaded model.
        :param dataframe: DataFrame containing the input data.
        :return: Prediction result.
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise MyException(e, sys)
