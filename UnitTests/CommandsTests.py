from __future__ import print_function
import unittest

from Helpers.Commands import ThreadedCommandFactory, Command, Kwargs
from SiteAutomations.Examples import GoogleExample
from Project import Models


class KwargsTest(unittest.TestCase):
    def setUp(self):
        self.test_dict = {
            'test1': 'hello world',
            'test2': 'zim zam kabam!'
        }
        self.kwarg_obj = Kwargs(self.test_dict)

    def test_iterate_over_object(self):
        self.assertEqual(type(self.kwarg_obj), Kwargs)
        for k, v in self.kwarg_obj:
            self.assertEqual(type(k), str)

    def test_instantiate_kwargs_object_with_invalid_input(self):
        self.assertRaises(TypeError, Kwargs, 'hello world')
        self.assertRaises(TypeError, Kwargs, u'hello world')
        self.assertRaises(TypeError, Kwargs, 123)
        self.assertRaises(TypeError, Kwargs, 1.00)

    def test_get_item_from_kwargs_object(self):
        self.assertEqual(self.kwarg_obj['test1'], 'hello world')
        self.assertEqual(self.kwarg_obj['test2'], 'zim zam kabam!')

    def test_set_item_from_kwargs_object(self):
        def set_kwargs_val(key, value):
            self.kwarg_obj[key] = value
            return self.kwarg_obj

        valid_output = {
            'test1': 'hello world',
            'test2': 'zim zam kabam!',
            'test3': 123
        }
        self.assertEqual(set_kwargs_val('test3', 123).dictionary, valid_output)

    def test_delete_item_from_kwargs_object(self):
        test_kwargs_object = Kwargs(self.kwarg_obj.dictionary)
        self.assertEqual(test_kwargs_object.__delitem__('test1').dictionary, {'test2': 'zim zam kabam!'})


class ThreadedCommandFactoryTest(unittest.TestCase):
    def setUp(self):
        self.controllers = {
            'goog1': GoogleExample.ThreadedGoogleSearch(Models),
            'goog2': GoogleExample.ThreadedGoogleSearch(Models)
        }

        self.cmd = ThreadedCommandFactory(self.controllers, False)

    def test_command_manager_attributes(self):
        self.assertEqual(type(self.cmd.controllers), dict)
        self.assertEqual(type(self.cmd.pool), list)

    def test_create_threads_with_invalid_inputs(self):
        def _(*args):
            print(args)
        self.assertRaises(TypeError, self.cmd.create_command, _, [1, 2, 3])
        self.assertRaises(TypeError, self.cmd.create_command, _, (1, 2, 3))
        self.assertRaises(TypeError, self.cmd.create_command, _, 234231)
        self.assertRaises(TypeError, self.cmd.create_command, _, 'jalsdkfoij')
        self.assertRaises(TypeError, self.cmd.create_command, _, u'asdfhosidjfn')
        self.assertRaises(TypeError, self.cmd.create_command, _, 0b1010110)

    def test_create_threads_with_valid_input(self):
        def _(*args, **kwargs):
            print(args)
            print(kwargs)
        command_pack = {
            'goog1': ('hello', Kwargs({'a': 1, 'b': 2, 'c': 3})),
            'goog2': ('hello world!',)
        }
        self.assertIsInstance(self.cmd.create_command(_, command_pack), Command)

    def tearDown(self):
        try:
            items = self.cmd.controllers.iteritems()
        except AttributeError:
            items = self.cmd.controllers.items()

        for k, controller in items:
            controller.driver.close()
            try:
                controller.driver.quit()
            except AttributeError:
                pass


def main():
    unittest.main()

if __name__ == '__main__':
    main()
