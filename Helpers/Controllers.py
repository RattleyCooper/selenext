from datetime import datetime
from Helpers.Commands import Kwargs
from selenium.webdriver.support.wait import WebDriverWait


def has_kwargs(func):
    """
    Decorator for passing **kwargs with your *args through the use of
    the Kwargs object.  Note that only 1 Kwargs object can be passed
    with the *args to the decorated function.  Any additional Kwargs
    objects will be ignored.

    :param func:
    :return:
    """

    def _process(*args):
        args = list(args)
        # Extract kwargs from args.
        d_args = [t for t in args if type(t) == Kwargs]
        try:
            d_args = d_args[0]
        except IndexError:
            return func(*args, **{})
        # Remove kwargs from args
        args = [item for item in args if type(item) != Kwargs]
        # Get args from Kwargs object.
        kwargs = {k: v for (k, v) in d_args}
        return func(*args, **kwargs)
    return _process


class IndependentController(object):
    """
    The base class for a threaded controller setup.
    """
    def attach_driver(self, driver, timeout=30):
        """
        Drivers must be attached after the controller has been instantiated so each controller has
        its own driver.  This will also attach a WebDriverWait to the class instance.

        :param driver:
        :param timeout:
        :return:
        """

        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
        return self


class BaseController(object):
    """
    The base class for a simple controller.
    """
    def __init__(self, driver, wait, models, logger):
        self.driver = driver
        self.wait = wait
        self.models = models
        self.logger = logger

    def _timestamp(self):
        """
        Generate a timestamp.

        :return:
        """

        ct = datetime.now()
        return ' '.join(ct.isoformat().split('T'))[:-7]
