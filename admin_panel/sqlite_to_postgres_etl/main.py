import os
import queue
from dotenv import load_dotenv

from extract import sqlite_extract
from transform import transform
from load import postgres_load

from admin_panel.sqlite_to_postgres_etl.logger import logger


load_dotenv()


if __name__ == '__main__':

    queue_transform = queue.Queue()
    queue_load = queue.Queue()

    sqlite_extract(
        src_data=os.environ.get('SQLITE_DB_NAME'),
        tables=os.environ.get('SQLITE_TABLES').split(','),
        queue_transform=queue_transform,
    )

    transform(
        queue_transform=queue_transform,
        queue_load=queue_load,
    )

    postgres_load(
        logger=logger,
        queue_load=queue_load,
        pg_database_config={
            'database': os.environ.get('POSTGRES_DB_NAME'),
            'user': os.environ.get('POSTGRES_DB_USER'),
            'password': os.environ.get('POSTGRES_DB_PASS'),
            'host': os.environ.get('POSTGRES_DB_HOST'),
            'port': os.environ.get('POSTGRES_DB_PORT'),
        },
    )
