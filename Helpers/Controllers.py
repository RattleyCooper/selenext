from random import uniform
from time import sleep
from .Commands import Kwargs
from selenium.webdriver.support.wait import WebDriverWait


# Generate a bunch of decorators for waiting up to 60 seconds.
for __ in range(1, 61):
    exec('''def waits{}(function):
    """
    A decorator for waiting {} second after function execution.  Great for waiting between actions.

    Args:
        function: function

    Returns:
        wait_decorator: function
    """

    def wait_decorator(*args, **kwargs):
        function_result = function(*args, **kwargs)
        sleep({})
        return function_result
    return wait_decorator'''.format(__, __, __))


def randomly_waits(function):
    """
    A decorator for waiting a random amount of time(0.1-3.01 seconds) after function execution.

    Args:
        function: function

    Returns:
        random_wait_decorator
    """

    def random_wait_decorator(*args, **kwargs):
        # Execute function and grab result
        function_result = function(*args, **kwargs)
        # Sleep
        sleep(uniform(0.01, 3.01))
        return function_result
    return random_wait_decorator


@randomly_waits
def human_fill(element, text):
    """
    Send keys to an element and wait a random amount of time afterwards.

    Args:
        element:
        text:

    Returns:

    """

    return element.send_keys(text)


@randomly_waits
def human_click(element):
    """
    Click on an element and wait a random amount of time afterwards.

    Args:
        element:

    Returns:

    """

    return element.click()



def has_kwargs(function):
    """
    Decorator for passing **kwargs with your *args through the use of
    the Kwargs object.  Note that only 1 Kwargs object can be passed
    with the *args to the decorated function.  Any additional Kwargs
    objects will be ignored.

    Args:
        function: function

    Returns:
        kwargsable: function
    """

    # Define a local function within has_kwargs
    def kwargsable(*args, **kwargs):
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
                return function(*args, **{})

        # Remove kwargs from args
        args = [item for item in args if type(item) != Kwargs]

        # Get kwargs from the dictionary args if default kwargs aren't used
        if kwargs_len == 0:
            kwargs = {k: v for (k, v) in d_args}
        # Execute the func, which is some_controller_func
        return function(*args, **kwargs)

    # Return the local callable function `_process`
    return kwargsable


class IndependentController(object):
    """
    The base class for a threaded controller setup.
    """
    def attach_driver(self, driver, timeout=30):
        """
        Drivers must be attached after the controller has been instantiated so each controller has
        its own driver.  This will also attach a WebDriverWait to the class instance.

        Args:
            driver: Selenium WebDriver
            timeout: int

        Returns:
            self
        """

        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
        return self

    def call(self, method_name, *args, **kwargs):
        """
        Call one of the controller's methods with the given *args or **kwargs

        Args:
            method_name:
            *args:
            **kwargs:

        Returns:
            method results
        """

        # Grab the method from self.
        method = getattr(self, method_name)

        # Determine how to call the method and return the results.
        if args and kwargs:
            return method(*args, **kwargs)
        elif args and not kwargs:
            return method(*args)
        elif kwargs and not args:
            return method(**kwargs)
        else:
            return method()
