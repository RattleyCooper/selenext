

class DummyLogger(object):
    """
    A logger that does absolutely nothing.  Meant as a drop in replacement for a
    logger that you would normally get from the logging module.
    """
    def __init__(self, prints=True):
        self.prints = prints

    def info(self, *args):
        if self.prints:
            print args
        return self

    def warn(self, *args):
        if self.prints:
            print args
        return self

    def error(self, *args):
        if self.prints:
            print args
        return self

    def debug(self, *args):
        if self.prints:
            print args
        return self