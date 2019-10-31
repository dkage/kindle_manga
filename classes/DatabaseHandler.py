import configparser
import psycopg2


class DatabaseHandlers:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config/postgres_conn.ini')
