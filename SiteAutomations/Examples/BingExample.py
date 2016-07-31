from time import sleep
from random import randint
from Helpers.Controllers import ThreadedController


def _do_search(driver, wait, search_term):
    """
    Perform a Bing Search.

    :param driver:
    :param wait:
    :param search_term:
    :return:
    """
    driver.get('http://www.bing.com/')

    search_input = driver.find_element_by_name('q')
    search_button = driver.find_element_by_id('sb_form_go')

    search_input.send_keys(search_term)
    sleep(randint(1, 2))
    search_button.click()

    wait.until(lambda driver: driver.find_element_by_xpath('//span[@class="sb_count"]').is_displayed())
    return True


class BingSearch(object):
    def __init__(self, driver, wait, models):
        self.driver = driver
        self.wait = wait
        self.models = models

    def do_search(self, search_term):
        return _do_search(self.driver, self.wait, search_term)


class ThreadedBingSearch(ThreadedController):
    def __init__(self, models):
        self.models = models

    def do_search(self, search_term):
        return _do_search(self.driver, self.wait, search_term)
