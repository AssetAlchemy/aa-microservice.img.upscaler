from pymongo import MongoClient
import gridfs

from bson.objectid import ObjectId

from files.domain.file import File
from files.domain.file_repository import FileRepository


class MongoFileRepository(FileRepository):
    def __init__(self, db_uri: str, db_name: str):
        self._client = None
        self._db = None
        self._fs = None
        self.db_uri = db_uri
        self.db_name = db_name

    def _connect(self):
        """Connect to mongo if is necessary."""
        if self._client is None or self._db is None or self._fs is None:
            # Connecting to database
            self._client = MongoClient(self.db_uri)
            self._db = self._client[self.db_name]

            # Creating gridFS object
            self._fs = gridfs.GridFS(self._db, "uploads")

    def add(self, file: File) -> File:
        self._connect()
        metadata = {"filename": file.filename, "_id": ObjectId(file.file_id)}
        self._fs.put(file.content, **metadata)
        return file

    def get(self, file_id: str) -> File:
        self._connect()
        file = self._fs.find_one({"_id": ObjectId(file_id)})
        if not file:
            return None
        filemetadata = self._db.uploads.files.find_one({"_id": ObjectId(file_id)})
        return File(
            file_id=file_id, filename=filemetadata["filename"], content=file.read()
        )
