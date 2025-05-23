import os
from minio import Minio
from abc import ABCMeta, abstractmethod
from app.domain.entity import UploadFile
from app.infra.config.base import settings

class Storage(metaclass=ABCMeta):

    @abstractmethod
    def save(self, upload_file: UploadFile) -> str:
        ...

    @abstractmethod
    def get_uri(self) -> str:
        ...


class MinioStorage(Storage):
    
    minio_client: Minio
    __bucket: str = settings.STORAGE_BUCKET
    
    def __init__(self):
        super().__init__()
        self.minio_client = Minio(
            f'{settings.STORAGE_HOST}:{settings.STORAGE_PORT}',
            access_key=settings.STORAGE_ACCESS_KEY,
            secret_key=settings.STORAGE_SECRET_KEY,
            secure=False
        )
        self.__check_bucket()

    def __check_bucket(self) -> None:
        if not self.minio_client.bucket_exists(self.__bucket):
            self.minio_client.make_bucket(self.__bucket)
            self.minio_client.set_bucket_policy(
                self.__bucket,
                f'{{"Version":"2012-10-17","Statement":[{{"Effect":"Allow","Principal":{{"AWS":"*"}},"Action":"s3:GetObject","Resource":"arn:aws:s3:::{self.__bucket}/*"}}]}}'
            )

    def get_uri(self) -> str:
        return f'http://{settings.STORAGE_HOST}:{settings.STORAGE_PORT}/{self.__bucket}/'

    def save(self, upload_file: UploadFile) -> str:
        self.minio_client.put_object(
            self.__bucket, upload_file.get_file_path(), upload_file.file, upload_file.size
        )

        return f'{self.__bucket}/{upload_file.get_file_path()}'
