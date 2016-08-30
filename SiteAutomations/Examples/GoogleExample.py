"""
This is an example of what the a `SiteAutomation` might look like
using Slack.  This controller is pretty bare-bones.
"""

from __future__ import print_function
from time import sleep
from random import randint
from ...Helpers.Controllers import IndependentController, has_kwargs


def _do_search(driver, wait, search_term):
    """
    Perform a Google search.

    :param driver:
    :param wait:
    :param search_term:
    :return:
    """
    driver.get('https://google.com')

    sleep(randint(1, 2))

    # Type search
    search_input = driver.find_element_by_name('q')
    search_input.send_keys(search_term)

    sleep(randint(1, 2))

    # Click search button.
    search_button = driver.find_element_by_name('btnG')
    search_button.click()
    wait.until(lambda the_driver: the_driver.find_element_by_id('resultStats').is_displayed())
    return True


class GoogleSearch(object):
    """
    This Controller needs a WebDriver instance, WebDriverWait instance,
    and the collection of Models in order to work.
    """
    def __init__(self, driver, wait, models):
        # Set up driver.
        if driver.__class__.__name__ != 'WebDriver':
            err = "{} is not an instance of WebDriver.".format(str(driver))
            raise TypeError(err)
        self.driver = driver
        self.wait = wait
        self.models = models

    def do_search(self, search_term):
        return _do_search(self.driver, self.wait, search_term)


class ThreadedGoogleSearch(IndependentController):
    """
    Note that if you inherit from IndependentController, you can use
    the CommandManager or ThreadedCommandManager to perform requests
    with their own WebDriver instances.
    """
    def __init__(self, models):
        self.models = models

    # Using the @has_kwargs decorator allows keyword arguments to be
    # passed to the method.  When you assemble a command pack for the
    # CommandManager, just include an instance of the Kwargs object.
    @has_kwargs
    def do_search(self, search_term, some_kwarg='some value'):
        print(some_kwarg)
        return _do_search(self.driver, self.wait, search_term)
