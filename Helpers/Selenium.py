from selenium.common.exceptions import TimeoutException
from Config.Environment import env


# todo: Remove custom waits.  There has to be a better way of doing this.
class CustomWait(object):
    def __init__(self, wait, mailer, tries=3):
        self.wait = wait
        self.mailer = mailer
        self.tries = tries

    def until(self, method, tries=3):
        """
        A custom wait wrapper for selenium waits.  It enables waits to be tried multiple times.

        :param method:
        :param tries:
        :return:
        """
        if tries > self.tries:
            the_tries = tries
        else:
            the_tries = self.tries

        for i in range(0, the_tries):
            try:
                self.wait.until(method)
                return self
            except TimeoutException:
                pass

        msg = "A custom wait timed out after {} tries.".format(the_tries)
        self.mailer.send_email(env("ADMIN_EMAIL"), "Slack Project Error!", msg)
        return self

    def until_not(self, method, tries=3):
        if tries > self.tries:
            the_tries = tries
        else:
            the_tries = self.tries

        for i in range(0, the_tries):
            try:
                self.wait.until_not(method)
                return self
            except TimeoutException:
                pass

        msg = "A custom wait timed out after {} tries.".format(the_tries)
        self.mailer.send_email(env("ADMIN_EMAIL"), "Slack Project Error!", msg)
        return self