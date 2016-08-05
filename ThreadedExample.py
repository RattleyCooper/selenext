"""
Slack is a micro-framework for scraping the web using selenium.
Written by Wykleph in April of 2016.

Create models in the `Models.py` file.

Once you have defined your models, they are accessed using the
`Models.ModelName` syntax.
"""

from time import sleep
# Database models used to interact with databases.
from Project import Models
# Controllers are kept in the SiteAutomations folder.
from SiteAutomations.Examples import GoogleExample, BingExample
# Pull in the command factory, which is the backbone to threaded automations.
# also pull in the Kwargs object for passing kwargs into commands.
from Helpers.Commands import ThreadedCommandFactory, Kwargs

# Define some controllers to pass to ThreadedCommandFactory.
# Note that the controllers being used are subclasses of IndependentController.
# These classes don't handle any threading, but they are set up so that the threaded
# command factory will be able to create threaded commands.
controllers = {
    'google': GoogleExample.ThreadedGoogleSearch(Models),
    'bing': BingExample.ThreadedBingSearch(Models)
}
cmd_factory = ThreadedCommandFactory(controllers, logging=False)

# Register arguments to pass to each controller.  They are
# matched by the key in the controllers dictionary.
# The next search_command shows how to add kwargs to
# the command pack.
search_command_1 = {
    'google': ('google wiki',),
    'bing': ('bing wiki',)
}

# Each argument is passed as *args.  If you need any
# **kwargs, just instantiate a Kwargs object with the
# dictionary containing the **kwargs.
search_command_2 = {
    'google': ('star wars', Kwargs({'some_kwarg': 'Overridden value!!!'})),
    'bing': ('star wars',)
}

# Create the threads.  A Command instance is returned when
# the threads are created.  These Command objects are used
# to start the threads.  Pass a function as the first
# parameter and the command pack as *args.
cmd1 = cmd_factory.create_command(lambda controller, *search_term: controller.do_search(*search_term), search_command_1)
cmd2 = cmd_factory.create_command(lambda controller, *search_term: controller.do_search(*search_term), search_command_2)

# Start the threads.  Each search will be executed, and it will
# only take as long as the longest automation time.
cmd1.start()
print 'finished first search'
sleep(3)
cmd2.start()
print 'finished second search'
sleep(5)

# Close the WebDrivers down.
cmd_factory.shutdown()
