from Config.Environment import env, env_driver
import threading


class ThreadedCommandManager(object):
    """
    Used for running threaded commands.  Each controller must use a separate instance of WebDriver.

    Example:
        controllers = {
            'google': google_controller,
            'yahoo': yahoo_controller
        }
        thread_manager = ThreadedControllerManager(controllers, attach_drivers=True)
    """
    def __init__(self, controllers, logging, attach_drivers=True, wait_timeout=30, log_file='multithread_log.txt'):
        if type(controllers) != dict:
            raise TypeError('controllers must be a dictionary of controllers.')

        if logging:
            # Set up the logger #
            logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger(ThreadedCommandManager.__name__)

            # Create log handler for writing to file. #
            handler = logging.FileHandler(log_file)
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
            # This will just print the logged stuff to the console.
            self.logger = self

        self.controllers = controllers
        self.wait_timeout = wait_timeout
        self.thread_pool = []
        if attach_drivers:
            self.logger.info('Attaching drivers.')
            self._attach_drivers()
            self.logger.info('Drivers attached.')

    def info(self, something):
        print something
        return self

    def warn(self, something):
        print something
        return self

    def error(self, something):
        print something
        return self

    def debug(self, something):
        print something
        return self

    def _attach_drivers(self):
        """
        Attach separate drivers to each controller.

        :return:
        """
        for key, args in self.controllers.iteritems():
            if 'attach_driver' in dir(args):
                args.attach_driver(env_driver(env('BROWSER'))(), timeout=self.wait_timeout)

    def create_threads(self, target, command_pack):
        """
        Create threads for the given target function.  The command pack is used to provide args
        to the target function.

        Example of basic setup:

        def do_login(controller, username, password):
            return controller.do_login(username, password)

        m = ThreadedControllerManager({
                'google': google_controller,
                'bing': bing_controller
            }
        )
        do_login_command = {
            'google': ('google_username', 'google_password'),
            'bing': ('bing_username', 'bing_password')
        }
        m.create_threads(do_login, do_login_command)
        m.start_threads()

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
            self.thread_pool.append(thread)
        return self

    def start_threads(self, dump_threads=False, join_threads=True):
        self.logger.info('Starting threads.')
        for thread in self.thread_pool:
            thread.start()
        if join_threads:
            self.logger.info('Joining threads.')
            for i, thread in enumerate(self.thread_pool):
                thread.join()
                self.logger.debug('Thread #{} joined: {}'.format(i, thread))
        if dump_threads:
            self.logger.debug('Dumping threads.')
            self.dump_threads()
        return self

    def dump_thread(self, thread):
        """
        Remove a thread from the pool of threads.

        :param thread:
        :return:
        """
        self.logger.info('Removing thread.')
        self.thread_pool.remove(thread)
        self.logger.info('Thread removed.')
        return self

    def dump_threads(self):
        self.thread_pool = []
        self.logger.info('Threads dumped, 0 threads in pool.')
        return self
