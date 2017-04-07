from os import getcwd
from .common import EnvironmentContainer
from .common import ConfigParser


__SELENEXT_FRAMEWORK_ENV_PATH = getcwd()\
                                 .replace('\\', '/')\
                                 .replace('SiteAutomations', '')\
                                 .replace('Jobs', '')

__SELENEXT_FRAMEWORK_ENV_PATH += '/.env' if __SELENEXT_FRAMEWORK_ENV_PATH[-1] != '/' else '.env'


if EnvironmentContainer.container == {}:
    ConfigParser(EnvironmentContainer, filepath=__SELENEXT_FRAMEWORK_ENV_PATH).load()


def env(variable_name, func=lambda x: x):
    """
    Get the corresponding environment variable.  Pass a function
    like `int` or `bool` as the `type_hint` keyword argument to
    automatically run that function on the output.

    Args:
        variable_name: string
        func: function

    Returns:
        string
    """
    
    return func(EnvironmentContainer.container[variable_name])


def env_driver(browser):
    """
    Return the web driver.

    Args:
        browser: string

    Returns:
        selenium WebDriver
    """

    from selenium import webdriver

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
    """
    Get the database object that should be used.

    Args:
        db_type: string

    Returns:
        peewee database driver.
    """

    db = False
    if db_type == 'sql':
        from peewee import SqliteDatabase

        db = SqliteDatabase(env("DB"))

    elif db_type == 'mysql':
        from peewee import MySQLDatabase

        db = MySQLDatabase(
            env("DB"),
            host=env("DB_HOST"),
            port=int(env("DB_PORT")),
            user=env("DB_USERNAME"),
            passwd=env("DB_PASSWORD")
        )

    elif db_type == 'postgresql':
        from peewee import PostgresqlDatabase

        db = PostgresqlDatabase(
            env('DB'),
            host=env("DB_HOST"),
            port=int(env("DB_PORT")),
            user=env("DB_USERNAME"),
            passwd=env("DB_PASSWORD")
        )

    elif db_type == 'berkeley':
        from playhouse.berkeleydb import BerkeleyDatabase

        db = BerkeleyDatabase(
            env('DB'),
            host=env("DB_HOST"),
            port=int(env("DB_PORT")),
            user=env("DB_USERNAME"),
            passwd=env("DB_PASSWORD")
        )

    return db
