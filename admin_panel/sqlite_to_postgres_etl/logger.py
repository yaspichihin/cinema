import os
import logging
from dotenv import load_dotenv


load_dotenv()


logging.basicConfig(
    level=os.environ.get('DEBUG_LEVEL'),
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='load_data.log',
    encoding='utf-8',
)

logger = logging.getLogger('sqlite_to_postgres_etl')
