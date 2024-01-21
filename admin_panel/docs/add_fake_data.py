import contextlib
import random
import uuid
import psycopg2
from datetime import datetime
from faker import Faker
from psycopg2.extras import execute_batch

fake = Faker()

# Подготавливаем DSN (Data Source Name) для подключения к БД Postgres
dsn = {
    'dbname': 'films',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432,
    'options': '-c search_path=content',
}

PERSONS_COUNT = 100000
PAGE_SIZE = 5000

now = datetime.utcnow()

# Установим соединение с БД используя контекстный менеджер with.
# В конце блока автоматически закроется курсор (cursor.close())
# и соединение (contextlib.closing вызовет conn.close())
with contextlib.closing(psycopg2.connect(**dsn)) as conn, conn.cursor() as cur:

    # Заполнение таблицы Person
    persons_ids = [str(uuid.uuid4()) for _ in range(PERSONS_COUNT)]
    query = 'INSERT INTO person (id, fullname, created, modified) VALUES (%s, %s, %s, %s)'
    data = [(pk, fake.last_name(), now, now) for pk in persons_ids]
    execute_batch(cur, query, data, page_size=PAGE_SIZE)
    conn.commit()

    # Заполнение таблицы PersonFilm
    person_film_data = []
    roles = ['actor', 'producer', 'director']
    cur.execute('SELECT id FROM film')
    film_ids = [data[0] for data in cur.fetchall()]

    for film_id in film_ids:
        for person_id in random.sample(persons_ids, 5):
            role = random.choice(roles)
            person_film_data.append((str(uuid.uuid4()), film_id, person_id, role, now))

    query = 'INSERT INTO person_film (id, film_id, person_id, role, created) VALUES (%s, %s, %s, %s, %s)'
    execute_batch(cur, query, person_film_data, page_size=PAGE_SIZE)
    conn.commit()
