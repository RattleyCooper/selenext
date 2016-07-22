import unittest
from Config.Environment import env, env_driver, get_database
from selenium import webdriver
from peewee import SqliteDatabase


class ConfigLoaderTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_env_no_key(self):
        self.assertRaises(KeyError, env, 'DUR')

    def test_env(self):
        self.assertEqual(env('BROWSER'), 'chrome')

    def test_env_driver(self):
        self.assertEqual(env_driver(env('BROWSER')), webdriver.Chrome)

    def test_env_driver_no_browser(self):
        self.assertEqual(env_driver(env('DB')), False)

    def test_get_database(self):
        self.assertIsInstance(get_database(env('DB_TYPE')), SqliteDatabase)

    def test_get_database_wrong_input(self):
        self.assertEqual(get_database(env('BROWSER')), False)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
