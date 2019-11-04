import configparser
import psycopg2


class DatabaseHandler:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config/postgres_conn.ini')
        self.kindle_user = dict(config['postgres'])
        # Checks for admin key. Not obligatory to be used as it is only used during first setup.
        try:
            self.admin = dict(config['postgres_admin'])
        except KeyError:
            self.admin = []


    def print_users(self):
        print(self.admin)
        print(self.kindle_user)



