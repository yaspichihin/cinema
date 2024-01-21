from uuid import uuid4
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GenreFilm:
    id: uuid4
    genre_id: str
    film_id: str
    created: datetime
