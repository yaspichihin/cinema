from uuid import uuid4
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PersonFilm:
    id: uuid4
    person_id: str
    film_id: str
    person_role: str
    created: datetime
