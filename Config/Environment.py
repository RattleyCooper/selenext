from selenium import webdriver
from peewee import *

ENV_PATH = __file__\
    .replace('Config\\', '.env')\
    .replace('Environment.pyc', '')\
    .replace('Environment.py', '')


class ConfigLoader:
    """ Create a mapping of the  """
    def __init__(self, filepath='.env'):
        self.lines = {}
        with open(filepath, 'r') as f:
            for line in f:
                if line[0] == '#':
                    continue
                if '=' in line:
                    line_pieces = line.split('=')
                    self.lines[line_pieces[0]] = '='.join(line_pieces[1:]).strip()

    def get(self, variable_name):
        return self.lines[variable_name]

RESOURCE_LOADER = ConfigLoader(filepath=ENV_PATH)


def env(variable_name):
    """ Get the corresponding environment variable. """

    return RESOURCE_LOADER.get(variable_name)


def env_driver(browser):
    """ Return the web driver. """

    the_driver = False
    if browser == 'chrome':
        the_driver = webdriver.Chrome
    elif browser == 'firefox':
        the_driver = webdriver.Firefox
    elif browser == 'safari':
        the_driver = webdriver.Safari
    elif browser == 'phantomjs':
        the_driver = webdriver.PhantomJS
    elif browser == 'opera':
        the_driver = webdriver.Opera
    return the_driver


def get_database(db_type):
    """ Get the database object that should be used. """

    db = False
    if db_type == 'sql':
        db = SqliteDatabase(env("DB"))
    elif db_type == 'mysql':
        db = MySQLDatabase(
            env("DB"),
            host=env("DB_HOST"),
            port=env("DB_PORT"),
            user=env("DB_USERNAME"),
            passwd=env("DB_PASSWORD")
        )
    elif db_type == 'postgresql':
        db = PostgresqlDatabase(
            env('DB'),
            host=env("DB_HOST"),
            port=env("DB_PORT"),
            user=env("DB_USERNAME"),
            passwd=env("DB_PASSWORD")
        )
    elif db_type == 'berkeley':
        from playhouse.berkeleydb import BerkeleyDatabase
        db = BerkeleyDatabase(
            env('DB'),
            host=env("DB_HOST"),
            port=env("DB_PORT"),
            user=env("DB_USERNAME"),
            passwd=env("DB_PASSWORD")
        )
    return db
