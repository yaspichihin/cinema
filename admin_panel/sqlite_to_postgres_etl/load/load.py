import queue
import psycopg2
from typing import Any
from dataclasses import astuple, fields
import logging

import admin_panel.sqlite_to_postgres_etl.etl_dataclasses as datacls


def get_stmt(obj: Any, cursor) -> str:
    stmt = ''
    obj_type = type(obj)

    column_names = [field.name for field in fields(obj)]
    column_names_str = ', '.join(column_names)

    col_count = ', '.join(['%s'] * len(column_names))
    bind_values = cursor.mogrify(f"({col_count})", astuple(obj)).decode('utf-8')

    match obj_type:

        case obj_type if obj_type == datacls.Genre:
            stmt = f'''
            INSERT INTO content.genre ({column_names_str}) VALUES
            {bind_values}
            ON CONFLICT (id) DO NOTHING;
            '''

        case obj_type if obj_type == datacls.Person:
            stmt = f'''
            INSERT INTO content.person ({column_names_str}) VALUES
            {bind_values}
            ON CONFLICT (id) DO NOTHING;
            '''

        case obj_type if obj_type == datacls.Film:
            stmt = f'''
            INSERT INTO content.film ({column_names_str}) VALUES
            {bind_values}
            ON CONFLICT (id) DO NOTHING;
            '''

        case obj_type if obj_type == datacls.GenreFilm:
            stmt = f'''
            INSERT INTO content.genre_film ({column_names_str}) VALUES
            {bind_values}
            ON CONFLICT (id) DO NOTHING;
            '''

        case obj_type if obj_type == datacls.PersonFilm:
            stmt = f'''
            INSERT INTO content.person_film ({column_names_str}) VALUES
            {bind_values}
            ON CONFLICT (id) DO NOTHING;
            '''

    return stmt


def postgres_load(logger: logging, pg_database_config: dict, queue_load: queue.Queue) -> None:
    with psycopg2.connect(**pg_database_config) as pg_conn, pg_conn.cursor() as pg_curs:
        for _ in range(queue_load.qsize()):
            obj = queue_load.get()
            stmt = get_stmt(obj, pg_curs)

            try:
                pg_curs.execute(stmt)
                pg_conn.commit()

            except psycopg2.Error as err:
                print(err)
                print(stmt)
                pg_conn.rollback()
                message = (
                    f'{err.diag.sqlstate}-'
                    f'{err.diag.message_primary}-'
                    f'{stmt}'
                )
                logger.warning(message)
