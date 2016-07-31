import unittest
from Helpers.Mailers import GMailer


class GmailerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_mailer_set_up_with_invalid_inputs(self):
        self.assertRaises(TypeError, GMailer, 123, '123', 'smtp.gmail.com', 123)
        self.assertRaises(TypeError, GMailer, 'some_email', 11212, 'smtp.gmail.com', 123)
        self.assertRaises(TypeError, GMailer, 'some_email', 'some-password', 1231, 123)
        self.assertRaises(TypeError, GMailer, 'some_email', 'some-password', 'smtp.gmail.com', '123')

    def test_mailer_set_up_with_valid_inputs(self):
        m = GMailer('some_email', 'some-password', 'some.host.com', 123)
        self.assertEqual(type(m.username), str)
        self.assertEqual(type(m.password), str)
        self.assertEqual(type(m.host), str)
        self.assertEqual(type(m.port), int)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
