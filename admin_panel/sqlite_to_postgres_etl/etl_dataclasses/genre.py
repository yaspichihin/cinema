from uuid import uuid4
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Genre:
    id: uuid4
    name: str
    description: str
    created: datetime
    modified: datetime
