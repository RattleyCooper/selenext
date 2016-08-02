from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait


class ThreadedController(object):
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
