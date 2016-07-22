"""
Slack is a micro-framework for scraping the web using selenium.
Written by Wykleph in April of 2016.

Create models using `python genesis.py make:model ModelName.
The models are appended to the `Models.py` file, although
this will probably change to operate similar to the middleware
classes in the future.

Middleware for the models is generated when you create a model
and the files can be found in the `middleware` folder.  Methods
are automatically generated for each column that is defined on
a model and if you use the database helper, `Jambi`, the
middleware will run automatically.  Note that if you do not
want to have middleware generated for your models, you can pass
the `--no-middleware` flag when running `make:model`.

Once you have defined your models, they are accessed using the
`Models.ModelName` syntax.

In this file, an example of using `Jambi` to run peewee methods
is provided along with an example of booting up the framework
and running site automations.
"""

# todo: Have the .env file generate automatically and remove it from the repository.
# todo: Possibility of removing Jambi, as I haven't actually used it in any real life scenarios yet.
#       peewee and odbc work pretty well on their own.  That, and the fact that it is tightly coupled
#       with the Middleware module, it really isn't worth keeping.  It's much simpler to just keep
#       anything that the Middleware would do in the appropriate SiteAutomation.

from time import sleep
import Models
from Config.Environment import env, env_driver
from Helpers.Contexts import quitting
from Helpers.Database import Jambi
from SiteAutomations import GoogleExample
from selenium.webdriver.support.wait import WebDriverWait

jambi_user = Jambi(Models.User)

credentials = {
    'username': 'SomeGuyNamedBobby',
    'email': 'bobby@domain.com',
    'password': 'password_for_site'
}

# Know what data to expect, as Jambi will modify data differently
# depending on the Model function that is called.  I will be adding
# documentation on what returns what, however in a lot of cases, it
# just depends.  This will be changed in the future so that returned
# values are more consistent.
user = jambi_user.model_func('get_or_create', **credentials)
print user

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
    # Write your selenium code here.  Use Jambi to run peewee methods
    # to take advantage of the Middleware features, or just use peewee.

    # Here is an example of a `SiteAutomation` taken from the
    # `GoogleExample` site automation.  Check out the
    # `GoogleExample.py` file to find out how to use
    # the advanced filtering techniques that the
    # Validation module provides.
    google_search = GoogleExample.Search(driver, jambi_user)
    google_search.perform_search('google wiki')
    sleep(1)

    # The `scrape_wikipedia_href_results` method contains an example
    # of using the `WebElementFilter` class to do advanced filtering.
    results = google_search.scrape_wikipedia_href_results()
    print results
    sleep(2)
    pass
