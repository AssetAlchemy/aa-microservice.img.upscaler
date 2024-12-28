from dataclasses import dataclass, field

from bson.objectid import ObjectId


@dataclass
class File:
    file_id: str = field(default_factory=lambda: str(ObjectId()))
    filename: str = field(default_factory=lambda: "")
    content: bytes = field(default_factory=lambda: b"")
