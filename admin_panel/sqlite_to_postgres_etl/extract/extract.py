import queue
import sqlite3
from contextlib import contextmanager

import admin_panel.sqlite_to_postgres_etl.etl_dataclasses as datacls


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def get_dataclass_obj(table, row_with_headers: dict):
    match table:
        case 'genre':
            return datacls.Genre(
                id=row_with_headers.get('id'),
                name=row_with_headers.get('name'),
                description=row_with_headers.get('description'),
                created=row_with_headers.get('created_at'),
                modified=row_with_headers.get('updated_at'),
            )
        case 'person':
            return datacls.Person(
                id=row_with_headers.get('id'),
                fullname=row_with_headers.get('full_name'),
                created=row_with_headers.get('created_at'),
                modified=row_with_headers.get('updated_at'),
            )
        case 'film_work':
            return datacls.Film(
                id=row_with_headers.get('id'),
                title=row_with_headers.get('title'),
                description=row_with_headers.get('description'),
                creation_date=row_with_headers.get('created_date'),
                rating=row_with_headers.get('rating'),
                film_type=row_with_headers.get('type'),
                created=row_with_headers.get('created_at'),
                modified=row_with_headers.get('updated_at'),
            )
        case 'person_film_work':
            return datacls.PersonFilm(
                id=row_with_headers.get('id'),
                person_id=row_with_headers.get('person_id'),
                film_id=row_with_headers.get('film_work_id'),
                person_role=row_with_headers.get('role'),
                created=row_with_headers.get('created_at'),
            )
        case 'genre_film_work':
            return datacls.GenreFilm(
                id=row_with_headers.get('id'),
                genre_id=row_with_headers.get('genre_id'),
                film_id=row_with_headers.get('film_work_id'),
                created=row_with_headers.get('created_at'),
            )


def sqlite_extract(src_data: str, tables: list, queue_transform: queue.Queue) -> None:
    with conn_context(src_data) as conn:
        curs = conn.cursor()

        for table in tables:
            stmt = f'SELECT * FROM {table};'
            curs.execute(stmt)
            data = curs.fetchall()

            for row in data:
                obj = get_dataclass_obj(table, dict(row))
                queue_transform.put(obj)
