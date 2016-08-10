from .Commands import Kwargs
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

    # Define a local function within has_kwargs
    def _process(*args, **kwargs):
        args = list(args)
        # Extract kwargs from args.
        d_args = [thing for thing in args if type(thing) == Kwargs]

        # Check if default kwargs should be used.
        kwargs_len = len(kwargs)
        if kwargs_len == 0:
            # If there is a Kwargs instance in the list then process the kwargs
            try:
                d_args = d_args[0]  # Pop the Kwargs instance off the list
            except IndexError:
                # func is equal to some_controller_func
                return func(*args, **{})

        # Remove kwargs from args
        args = [item for item in args if type(item) != Kwargs]

        # Get kwargs from the dictionary args if default kwargs aren't used
        if kwargs_len == 0:
            kwargs = {k: v for (k, v) in d_args}
        # Execute the func, which is some_controller_func
        return func(*args, **kwargs)

    # Return the local callable function `_process`
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
