from typing import Optional

from files.domain.file_repository import FileRepository
from files.domain.file import File


class SaveFileCommand:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    def execute(self, filename: str, content: str) -> str:
        try:
            file = File(filename=filename, content=content)
            saved_file = self.file_repository.add(file)
            return str(saved_file.file_id)
        except Exception as e:
            print(e)
            raise Exception("Error to save file")


class GetFileCommand:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    def execute(self, file_id: str) -> Optional[File]:
        try:
            return self.file_repository.get(file_id)
        except Exception:
            raise Exception("Error to get file")
