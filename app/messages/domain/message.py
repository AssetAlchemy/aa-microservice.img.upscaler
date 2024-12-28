from dataclasses import dataclass, field
from typing import Literal

from bson.objectid import ObjectId


@dataclass
class Message:
    asset_id: ObjectId = field(default_factory=lambda: ObjectId())
    options: dict = field(default_factory=lambda: {})
    status: Literal["normal", "error"] = field(default_factory="error")
