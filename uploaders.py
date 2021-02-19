from abc import ABC, abstractmethod
from io import BytesIO

from flask import current_app


class FileStorage(ABC):
    @abstractmethod
    def upload_file(self, file) -> str:
        """
        Uploads passed file to its destination.
        :param file:
        :return: file url
        """
        pass

    @abstractmethod
    def retrieve_file(self, file_location):
        """
        Retrieves file from the storage
        :param file_location:
        :return: BytesIO
        """
        pass


class FileSystemStorage(FileStorage):
    def __init__(self):
        self._upload_path = current_app.config['FILE_UPLOAD_PATH']

    def upload_file(self, file) -> str:
        file_path = f"{self._upload_path}/{file.filename}"
        file.save(file_path)
        return file_path

    def retrieve_file(self, file_location):
        try:
            file = open(file_location or "", "rb")
            file_bytes = BytesIO(file.read())
            return file_bytes
        except FileNotFoundError:
            return None
