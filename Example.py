from __future__ import print_function
from time import sleep
# Database models used to interact with databases.
from Project import Models
# The environment variable loader.  These variables can be set in the .env file.
from Environment import env, env_driver
# Controllers are kept in the SiteAutomations folder.
from SiteAutomations.Examples import GoogleExample, BingExample
from Helpers.Contexts import quitting
# Pull in the command factory for the second example.
from Helpers.Commands import CommandFactory, Kwargs
from selenium.webdriver.support.wait import WebDriverWait

# This is where the WebDriver is instantiated. Instead
# of instantiating it directly, use the `env` and
# `env_driver` functions to grab it based on the
# `.env` configuration file.
# This could be written as:
#
#   browser = env("BROWSER")
#   web_driver = env_driver(browser)
#   with quitting(web_driver()) as driver:
#       pass
#
with quitting(env_driver(env("BROWSER"))()) as driver:
    wait = WebDriverWait(driver, 30)

    # Pass the web driver to the site automation along with anything
    # else it might need to do its job. This could include an
    # instance of WebDriverWait, and even the collection of
    # Models.
    google_search = GoogleExample.GoogleSearch(driver, wait, Models)
    bing_search = BingExample.BingSearch(driver, wait, Models)

    # Do stuff with your controllers.
    google_search.do_search('google wiki')
    sleep(5)
    bing_search.do_search('bing wiki')
    sleep(5)

# Optionally, you can use the command manager to do the searches.
# This will make each controller use it's own personal WebDriver.
# Define some controllers to pass to CommandFactory.
# Note that the controllers being used are subclasses of IndependentController.
# These classes don't handle any threading, but they are set up so that the
# command factory will be able to create commands with them.
controllers = {
    'google': GoogleExample.ThreadedGoogleSearch(Models),
    'bing': BingExample.ThreadedBingSearch(Models)  # Check out the example files for more info on threading.
}

# We use the CommandFactory instead of the ThreadedCommandFactory
# so that the each controller has it's own WebDriver instance
# and each request is made in the main thread.
cmd_factory = CommandFactory(controllers, logging=False)
# In addition to creating Command objects, instances of any CommandFactory object will
# act similar to how a dictionary works.  The only difference is you don't need to call
# iteritems() when iterating over it:
#
#       for key, controller in cmd_factory:
#           print key, controller
#
#       b = cmd_factory['bing']
#       b.do_search('hello world')
#
#       del cmd_factory['bing']
#       del cmd_factory['google']


# Register arguments to pass to each controller.  They are
# matched by the key in the controllers dictionary.
# Command packs are passed as *args.  If you need any
# **kwargs, just instantiate a Kwargs object with the
# dictionary containing the **kwargs and make sure
# the method you are calling with the command pack
# is decorated with @has_kwargs.
search_command = {
    'google': ('star wars', Kwargs({'some_kwarg': 'NEW KWARG VALUE!'})),  # You can override keyword arguments as well!
    'bing': ('star wars',)
}

# Create the command.  Pass a function as the first parameter and
# the command pack as the second parameter.  A Command instance
# is returned when the command is created.  These Command
# objects are used to start the work!
cmd = cmd_factory.create_command(lambda controller, *search_term: controller.do_search(*search_term), search_command)

# Start the command.  Each search will be executed one after the
# other.
cmd.start()
print('finished first search')
sleep(5)

# Close the WebDrivers down.
cmd_factory.shutdown()
