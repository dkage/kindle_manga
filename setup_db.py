import configparser
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# TODO create class for database connection
config = configparser.ConfigParser()
config.read('config/postgres_conn.ini')

# TODO Check postgres accessible
# TODO Check postgres_admin
# TODO If database not exists ? create : nothing
# TODO If user not exists ? create : nothing
# TODO Set user as owner of new database


# User to be passed from ini file needs to have CREATE DATABASE permissions
con = psycopg2.connect(dbname=config['postgres_admin']['database'],
                       user=config['postgres_admin']['user'],
                       host=config['postgres_admin']['host'],
                       password=config['postgres_admin']['password'])
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # This is needed to sql create database, as it needs autocommit

cur = con.cursor()
cur.execute(sql.SQL("CREATE DATABASE kindle_manga;"))

