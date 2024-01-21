from uuid import uuid4
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Person:
    id: uuid4
    fullname: str
    created: datetime
    modified: datetime
