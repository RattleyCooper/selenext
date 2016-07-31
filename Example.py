"""
Slack is a micro-framework for scraping the web using selenium.
Written by Wykleph in April of 2016.

Create models in the `Models.py` file.

Once you have defined your models, they are accessed using the
`Models.ModelName` syntax.
"""

from time import sleep
import Models
from Config.Environment import env, env_driver
from Helpers.Contexts import quitting
from SiteAutomations import GoogleExample
from selenium.webdriver.support.wait import WebDriverWait

# This is where selenium starts up.  Use the environment Helpers
# with the quitting context in order to ensure that the webdriver
# shuts down properly.  Depending on how it errors out, you may
# have to terminate lingering webdriver processes, however the
# quitting context should `close` and `quit` the driver.
# This could be written as:
#
#   browser = env("BROWSER")
#   web_driver = env_driver(browser)
#   with quitting(web_driver()) as driver:
#       pass
#
with quitting(env_driver(env("BROWSER"))()) as driver:
    # Write your selenium code here.

    # Here is an example of a `SiteAutomation` taken from the
    # `GoogleExample` site automation.  Check out the
    # `GoogleExample.py` file to find out how to use
    # the advanced filtering techniques that the
    # Validation module provides.
    wait = WebDriverWait(driver, 30)
    google_search = GoogleExample.GoogleSearch(driver, wait, Models)
    google_search.perform_search('google wiki')
    sleep(1)

    # The `scrape_wikipedia_href_results` method contains an example
    # of using the `WebElementFilter` class to do advanced filtering.
    results = google_search.scrape_wikipedia_href_results()
    print results
    sleep(2)
    pass
