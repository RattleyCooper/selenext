import unittest

from Helpers.Commands import ThreadedCommandFactory, Command
from SiteAutomations.Examples import GoogleExample
from Project import Models


class ThreadedCommandManagerTest(unittest.TestCase):
    def setUp(self):
        self.controllers = {
            'goog1': GoogleExample.ThreadedGoogleSearch(Models),
            'goog2': GoogleExample.ThreadedGoogleSearch(Models)
        }

        self.cmd = ThreadedCommandFactory(self.controllers, False)

    def test_command_manager_attributes(self):
        self.assertEqual(type(self.cmd.controllers), dict)
        self.assertEqual(type(self.cmd.thread_pool), list)

    def test_create_threads_with_invalid_inputs(self):
        def _(*args):
            print args
        self.assertRaises(TypeError, self.cmd.create_threads, _, [1, 2, 3])
        self.assertRaises(TypeError, self.cmd.create_threads, _, (1, 2, 3))
        self.assertRaises(TypeError, self.cmd.create_threads, _, 234231)
        self.assertRaises(TypeError, self.cmd.create_threads, _, 'jalsdkfoij')
        self.assertRaises(TypeError, self.cmd.create_threads, _, u'asdfhosidjfn')
        self.assertRaises(TypeError, self.cmd.create_threads, _, 0b1010110)

    def test_create_threads_with_valid_input(self):
        def _(*args):
            print args
        command_pack = {
            'goog1': ('hello',),
            'goog2': ('hello world!',)
        }
        self.assertIsInstance(self.cmd.create_threads(_, command_pack), Command)

    def tearDown(self):
        for k, controller in self.cmd.controllers.iteritems():
            controller.driver.close()
            try:
                controller.driver.quit()
            except AttributeError:
                pass


def main():
    unittest.main()

if __name__ == '__main__':
    main()
