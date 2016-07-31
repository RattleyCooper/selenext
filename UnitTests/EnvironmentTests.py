import unittest
from Config.Environment import env, env_driver, get_database
from selenium import webdriver
from peewee import SqliteDatabase


class ConfigLoaderEnvironmentTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_env_with_undefined_key(self):
        self.assertRaises(KeyError, env, 'DUR')

    def test_env_with_defined_key(self):
        self.assertEqual(env('BROWSER'), 'chrome')

    def test_env_driver_with_defined_browser(self):
        self.assertEqual(env_driver(env('BROWSER')), webdriver.Chrome)

    def test_env_driver_undefined_browser(self):
        self.assertEqual(env_driver(env('DB')), False)

    def test_get_database_with_defined_database_type(self):
        self.assertIsInstance(get_database(env('DB_TYPE')), SqliteDatabase)

    def test_get_database_with_undefined_database_type(self):
        self.assertEqual(get_database(env('BROWSER')), False)

    def tearDown(self):
        pass


def main():
    unittest.main()

if __name__ == '__main__':
    main()