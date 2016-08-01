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
from Helpers.Commands import ThreadedCommandFactory

# Define some controllers to pass to ThreadedCommandManager.
controllers = {
    'google': GoogleExample.ThreadedGoogleSearch(Models),
    'bing': BingExample.ThreadedBingSearch(Models)  # Check out the example files for more info on threading.
}
cmd_mgr = ThreadedCommandFactory(controllers, False)

# Register arguments to pass to each controller.  They are
# matched by the key in the controllers dictionary.
search_command_1 = {
    'google': ('google wiki',),
    'bing': ('bing wiki',)
}

search_command_2 = {
    'google': ('star wars',),
    'bing': ('star wars',)
}

# Create the threads.  Pass a function as the first parameter and
# the command pack as the second parameter.  A Command instance
# is returned when the threads are created.  These Command
# objects are used to start the threads.
cmd1 = cmd_mgr.create_threads(lambda controller, search_term: controller.do_search(search_term), search_command_1)
cmd2 = cmd_mgr.create_threads(lambda controller, search_term: controller.do_search(search_term), search_command_2)

# Start the threads.  Each search will be executed, and it will
# only take as long as the longest loading time.
cmd1.start_threads()
print 'finished first search'
sleep(3)
cmd2.start_threads()
print 'finished second search'
sleep(5)

# Close everything down.
cmd_mgr.shutdown()
