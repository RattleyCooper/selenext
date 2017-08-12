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
        sleep(uniform(0.99, 3.01))
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


class PageController(object):
    """
    Standard controller for controlling a page.
    """
    def __init__(self, page):
        self.page = page

    @randomly_waits
    def fill(self, element, text):
        """
        Send keys to an element, then randomly wait.

        Args:
            element:
            text:

        Returns:
            self
        """

        element.send_keys(text)
        return self

    @randomly_waits
    def click(self, element):
        """
        Click on an element, then randomly wait.

        Args:
            element:

        Returns:
            self
        """

        element.click()
        return self


class LoginPageController(PageController):
    """
    A generic controller for logging in to a webpage.  It uses a `Page` object and a
    `WebDriverWait` object to do the job.
    """
    def __init__(self, page):
        super(LoginPageController, self).__init__(page)

    @randomly_waits
    def do_login(self, username, password, remember_me=False, stay_logged_in=False, wait_func=False, navigate=False):
        """
        Log in to a web page using the given `Page` object as a template.  The `username` and `password`
        attributes must be set on the `Page` object along with an attribute that defines a `logged_in`
        `PageState`.  If you want to use the `remember_me` keyword arg, you must also have that attribute
        set on the `Page` object.  If you want the function to navigate to the login page and wait for the
        login form to be presented you need to set the `login_form_displayed` `PageState` and

        Args:
            username: str
            password: str
            remember_me: bool
            stay_logged_in: bool
            wait_func: func, bool
            navigate: bool

        Returns:
            self
        """

        if navigate:
            self.page.get(self.page.login_page)
            self.page.state.login_form_displayed.wait()

        self.fill(self.page.username, username)
        self.fill(self.page.password, password)

        # Click remember me checkbox
        if remember_me:
            self.click(self.page.remember_me)

        # Stay logged in checkbox
        if stay_logged_in:
            self.click(self.page.stay_logged_in)

        # Click login button
        self.page.login_button.click()

        # Call the wait function.
        if wait_func:
            self.wait.until(wait_func)

        self.page.state.logged_in.wait()

        return self
    

class SearchPageController(PageController):
    """
    A generic controller for a simple search page.  Just pass in your `Page` object
    with a `search_input` and a `search_button` defined, along with a `WebDriverWait`
    object.  You can call the `perform_search` method and it will fill in the input
    using the `Page` object passed in, then click the search button using the `Page`
    object.  You can also pass in the `wait_func` keyword to set a wait function that
    should be called before returning control.
    """
    def __init__(self, page, wait):
        super(SearchPageController, self).__init__(page, wait=wait)

    def perform_search(self, term, wait_func=False):
        """
        Search for the given term using the page object and the wait object if it is
        set.

        Args:
            term:
            wait_func:

        Returns:
            self
        """
        self.fill(self.page.search_input, term)
        self.page.search_button.click()

        if wait_func:
            self.wait.until(wait_func)

        return self


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
