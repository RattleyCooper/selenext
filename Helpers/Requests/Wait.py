

class RequestsWait(object):
    def __init__(self, driver, wait_time, poll_frequency=1, ignored_exceptions=None):
        self.driver = driver
        self.wait_time = wait_time
        self.poll_frequency = poll_frequency
        self.ignored_exceptions = ignored_exceptions

    def until(self, function, *args, **kwargs):
        try:
            return function(self.driver, *args, **kwargs)
        except AttributeError:
            return False

    def until_not(self, function, *args, **kwargs):
        try:
            return function(self.driver, *args, **kwargs)
        except AttributeError:
            return False
