"""
Slack is a micro-framework for scraping the web using selenium.
Written by Wykleph in April of 2016.

Create models in the `Models.py` file.

Once you have defined your models, they are accessed using the
`Models.ModelName` syntax.
"""

from time import sleep
# Database models used to interact with databases.
import Models
# The environment variable loader.  These variables can be set in the .env file.
from Config.Environment import env, env_driver
# Controllers are kept in the SiteAutomations folder.
from SiteAutomations.Examples import GoogleExample, BingExample
from Helpers.Contexts import quitting
from selenium.webdriver.support.wait import WebDriverWait

# This is where selenium starts up.
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
    # `GoogleExample.py` file.
    wait = WebDriverWait(driver, 30)
    # Pass the web driver to the site automation along with anything
    # else it might need to do its job. This could include an
    # instance of WebDriverWait, and even the collection of
    # Models.
    google_search = GoogleExample.GoogleSearch(driver, wait, Models)
    bing_search = BingExample.BingSearch(driver, wait, Models)
    google_search.do_search('google wiki')
    sleep(1)
    bing_search.do_search('bing wiki')
    sleep(1)
