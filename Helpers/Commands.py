from Config.Environment import env, env_driver
from Helpers import DummyLogger, DummyThread
import threading


class Kwargs(object):
    """
    An object used for passing **kwargs with your *args.

    Example:

    @has_kwargs
    def some_controller_func(first_arg, second_arg, some_arg=True, other_arg='NA'):
        print first_arg, second_arg
        print some_arg, other_arg

    a = ('hello', 'world', Kwargs({'some_arg': 'HELLO', 'other_arg': 'WORLD!!!'}))
    some_controller_func(*a)

    """
    def __init__(self, dictionary):
        try:
            dictionary.keys()
        except:
            raise TypeError('Kwargs requires a dictionary, got a {}'.format(type(dictionary)))
        self.dictionary = dictionary

    def __len__(self):
        return len(self.dictionary)

    def __getitem__(self, key):
        return self.dictionary[key]

    def __setitem__(self, key, value):
        self.dictionary[key] = value

    def __delitem__(self, key):
        del self.dictionary[key]

    def __iter__(self):
        return self.dictionary.iteritems()


class BaseCommandFactory(object):
    def __init__(self, controllers, logging=False, attach_drivers=True, wait_timeout=30, dummy_logger_prints=False, log_file='main_log.txt'):
        if type(controllers) != dict:
            raise TypeError('controllers must be a dictionary of controllers.')
        self.attach_drivers = attach_drivers
        self.log_file = log_file
        self.logging_val = logging
        if logging:
            # Set up the logger #
            logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger(ThreadedCommandFactory.__name__)

            # Create log handler for writing to file. #
            handler = logging.FileHandler(self.log_file)
            handler.setLevel(logging.DEBUG)

            # Create a logging format. #
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s.%(levelname)s: %(message)s',
                datefmt='%m-%d-%Y %H:%M:%S'
            )
            handler.setFormatter(formatter)

            # Add the handlers to the logger.
            logger.addHandler(handler)
            self.logger = logger
        else:
            self.logger = DummyLogger(prints=dummy_logger_prints, level=env('DUMMY_LOGGER_LEVEL'))

        self.controllers = controllers
        self.wait_timeout = wait_timeout
        self.pool = []
        if attach_drivers:
            self.logger.info('Attaching drivers.')
            self._attach_drivers()
            self.logger.info('Drivers attached.')

    def _shutdown_driver(self, key, retry=True):
        try:
            self.controllers[key].driver.close()
        except:
            pass
        try:
            self.controllers[key].driver.quit()
        except:
            pass
        if retry:
            self._shutdown_driver(key, retry=False)
        return self

    def __len__(self):
        return len(self.controllers)

    def __setitem__(self, key, value):
        self.controllers[key] = value

    def __getitem__(self, item):
        return self.controllers[item]

    def __delitem__(self, key):
        self._shutdown_driver(key)
        del self.controllers[key]

    def __iter__(self):
        return self.controllers.iteritems()

    def _attach_drivers(self):
        """
        Attach separate drivers to each controller.

        :return:
        """

        for key, args in self.controllers.iteritems():
            if 'attach_driver' in dir(args):
                args.attach_driver(env_driver(env('BROWSER'))(), timeout=self.wait_timeout)

    def shutdown(self):
        """
        Shut down teh WebDriver instances.

        :return:
        """

        for key, controller in self.controllers.iteritems():
            self._shutdown_driver(key)


class ThreadedCommandFactory(BaseCommandFactory):
    """
    Used for creating threaded commands.  Each controller must use a separate instance of WebDriver.

    Example:
        controllers = {
            'google': google_controller,
            'yahoo': yahoo_controller
        }
        thread_manager = ThreadedControllerManager(controllers, attach_drivers=True)
    """

    def create_command(self, target, command_pack):
        """
        Create threads for the given target function.  The command pack is used to provide args
        to the target function.

        Example of basic setup:

        def do_login(controller, username, password):
            return controller.do_login(username, password)

        m = ThreadedCommandFactory({
                'google': google_controller,
                'bing': bing_controller
            }
        )
        cmd = do_login_command = {
            'google': ('google_username', 'google_password'),
            'bing': ('bing_username', 'bing_password')
        }
        cmd = m.create_command(do_login, do_login_command)
        cmd.start()

        :param target:
        :param command_pack:
        :return:
        """

        if type(command_pack) != dict:
            raise TypeError('Expected a dictionary for the command_pack variable.')

        self.logger.info('Creating threads.')
        for key, args in command_pack.iteritems():
            args = (self.controllers[key],) + args
            thread = threading.Thread(target=target, args=args)
            self.pool.append(thread)

        # Swap variables.
        thread_pool, self.pool = self.pool, []

        return Command(self.logging_val, thread_pool, log_file=self.log_file)


class CommandFactory(BaseCommandFactory):
    def create_command(self, target, command_pack, dummy_logger_prints=False):
        """
        Create a command that will execute jobs one by one.
        
        :param target:
        :param command_pack:
        :param dummy_logger_prints:
        :return:
        """

        if type(command_pack) != dict:
            raise TypeError('Expected a dictionary for the command_pack variable.')

        self.logger.info('Creating command.')
        for key, args in command_pack.iteritems():
            args = (self.controllers[key],) + args
            thread = DummyThread(target=target, args=args)
            self.pool.append(thread)

        pool, self.pool = self.pool, []

        return Command(self.logging_val, pool, log_file=self.log_file, dummy_logger_prints=dummy_logger_prints)


class Command(object):
    def __init__(self, logging, pool, dummy_logger_prints=False, log_file='command_log.txt'):
        self.log_file = log_file
        if logging:
            # Set up the logger #
            logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger(Command.__name__)

            # Create log handler for writing to file. #
            handler = logging.FileHandler(self.log_file)
            handler.setLevel(logging.DEBUG)

            # Create a logging format. #
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s.%(levelname)s: %(message)s',
                datefmt='%m-%d-%Y %H:%M:%S'
            )
            handler.setFormatter(formatter)

            # Add the handlers to the logger.
            logger.addHandler(handler)
            self.logger = logger
        else:
            self.logger = DummyLogger(prints=dummy_logger_prints, level=env('DUMMY_LOGGER_LEVEL'))

        self.pool = pool

    def start(self, dump_pool=True, join_threads=True):
        """
        Start the threads in the thread pool.

        :param dump_pool:
        :param join_threads:
        :return:
        """

        self.logger.info('Starting command.')
        for thread in self.pool:
            thread.start()
        if join_threads:
            for i, thread in enumerate(self.pool):
                thread.join()
                self.logger.debug('Thread #{} joined: {}'.format(i, thread))
        if dump_pool:
            self.logger.debug('Dumping pool.')
            self.dump_pool()
        return self

    def dump_pool(self):
        """
        Remove the threads from the thread pool.

        :return:
        """

        self.pool = []
        self.logger.info('Threads dumped, 0 threads in pool.')
        return self
