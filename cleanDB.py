import csv
import psycopg2
import os

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()
cursor.execute('DROP DATABASE geodb')
cursor.execute('DROP USER geouser')
cursor.close()
conn.close()
