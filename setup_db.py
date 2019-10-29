import configparser
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE


# TODO create class for database connection
config = configparser.ConfigParser()
config.read('config/postgres_conn.ini')


con = psycopg2.connect(dbname='postgres',
                       user=config['postgres']['user'],
                       host=config['postgres']['host'],
                       password=config['postgres']['password'])

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
cur = con.cursor()

cur.execute(sql.SQL("CREATE DATABASE kindle_manga;"))

