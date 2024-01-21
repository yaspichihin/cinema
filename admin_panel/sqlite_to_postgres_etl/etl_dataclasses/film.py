from uuid import uuid4
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Film:
    id: uuid4
    title: str
    description: str
    creation_date: date
    rating: float
    film_type: str
    created: datetime
    modified: datetime
