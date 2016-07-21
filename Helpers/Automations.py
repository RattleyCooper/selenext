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
    def __init__(self, controllers, attach_drivers=True, wait_timeout=30):
        if type(controllers) != dict:
            raise TypeError('controllers must be a dictionary of controllers.')

        self.controllers = controllers
        self.wait_timeout = wait_timeout
        self.thread_pool = []
        if attach_drivers:
            self._attach_drivers()

    def _attach_drivers(self):
        """
        Attach separate drivers to each controller.

        :return:
        """
        for key, args in self.controllers.iteritems():
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

        for key, args in command_pack.iteritems():
            args = (self.controllers[key],) + args
            thread = threading.Thread(target=target, args=args)
            self.thread_pool.append(thread)

    def start_threads(self, dump_threads=False, join_threads=True):
        for thread in self.thread_pool:
            thread.start()
            if dump_threads:
                self.dump_thread(thread)
        if join_threads:
            for thread in self.thread_pool:
                thread.join()
        return self

    def dump_thread(self, thread):
        """
        Remove a thread from the pool of threads.

        :param thread:
        :return:
        """
        self.thread_pool.remove(thread)
        return self

    def dump_threads(self):
        self.thread_pool = []
        return self
