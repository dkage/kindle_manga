import configparser
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# TODO create class for database connection
config = configparser.ConfigParser()
config.read('config/postgres_conn.ini')

# User to be passed from ini file needs to have CREATE DATABASE permissions
con = psycopg2.connect(dbname='postgres',
                       user=config['postgres']['user'],
                       host=config['postgres']['host'],
                       password=config['postgres']['password'])
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # This is needed to sql create database, as it needs autocommit


cur = con.cursor()
cur.execute(sql.SQL("CREATE DATABASE kindle_manga;"))

