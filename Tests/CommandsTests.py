import unittest
from SiteAutomations import GoogleExample
from Helpers.Commands import ThreadedCommandManager


class ThreadedCommandManagerTest(unittest.TestCase):
    def setUp(self):
        self.controllers = {
            'goog1': GoogleExample.ThreadedGoogleSearch(),
            'goog2': GoogleExample.ThreadedGoogleSearch()
        }

        self.cmd = ThreadedCommandManager(self.controllers, False)

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
        self.assertEqual(self.cmd.create_threads(_, command_pack), self.cmd)

    def tearDown(self):
        for k, controller in self.cmd.controllers.iteritems():
            controller.driver.close()
            controller.driver.quit()

if __name__ == '__main__':
    unittest.main()
