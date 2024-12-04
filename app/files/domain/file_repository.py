import abc
from typing import Optional


from files.domain.file import File


class FileRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, file: File):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, file_id: str) -> Optional[File]:
        raise NotImplementedError
