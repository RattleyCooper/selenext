"""
This is an example of what the a `SiteAutomation` might look like
using Slack.

In this example, the `WebDriver` instance, along with the `Jambi`
instance are used to create methods for our main `Example.py`
file.

The class, `Helpers.Validation.WebElementFilter` is used in order to
filter element attributes.  The example is in the form of a list
comprehension, and can be found in the `scrape_wikipedia_href_results`
method.
"""

from time import sleep
from random import randint
from Helpers.Validation import WebElementFilter


class Search:
    def __init__(self, web_driver, jambi):
        # Set up driver.
        if web_driver.__class__.__name__ != 'WebDriver':
            err = "{} is not an instance of WebDriver.".format(str(web_driver))
            raise TypeError(err)
        self.web_driver = web_driver

        # Set up jambi.
        if jambi.__class__.__name__ != 'Jambi':
            err = "{} is not an instance of Jambi.".format(str(jambi))
            raise TypeError(err)
        self.jambi = jambi

        # Set up attribute filter.
        self.element_filter = WebElementFilter()

    def goto_search_page(self):
        """ Go to the google search page. """

        self.web_driver.get('https://google.com')
        return self

    def goto_image_search(self):
        """ Go to the google image search page. """

        # Go to the main google image search page with empty search
        # parameters.
        self.web_driver.get('https://www.google.com/imghp?tbm=isch')
        return self

    def scrape_wikipedia_href_results(self):
        """ Scrape the results from a google search. """

        # Find the <a> tags that are children of the <h3> tags.
        link_objects = self.web_driver.find_elements_by_xpath('//h3/a')

        # Set the pattern to scrape anything with 'wiki' in the href.
        pattern = '*wiki*'
        pattern2 = '.*Wikipedia, the free encyclopedia.*'

        # This is a working example of the `WebElementFilter` class
        # doing wildcard matches on link objects found using the
        # `find_elements` methods on an instance of `WebDriver`.
        # Extract link_objects in list comprehension, using wildcard
        # and regex matching.
        link_objects = [
            link_obj
            for link_obj in link_objects
            if self.element_filter.attribute('href').wildcard_match(link_obj, pattern) and
            self.element_filter.inner_text().regex_match(link_obj, pattern2)
        ]
        return [l.get_attribute('href') for l in link_objects]

    def perform_search(self, search_term, image_search=False):
        """ Perform an image search. """

        # Pick the search to perform.
        if not image_search:
            self.goto_search_page()
        else:
            self.goto_image_search()

        sleep(randint(3, 15))

        # Type search
        search_input = self.web_driver.find_element_by_name('q')
        search_input.send_keys(search_term)

        sleep(randint(3, 15))

        # Click search button.
        search_button = self.web_driver.find_element_by_name('btnG')
        search_button.click()
        return self
