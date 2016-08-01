

class DummyLogger(object):
    """
    A logger that does absolutely nothing.  Meant as a drop in replacement for a
    logger that you would normally get from the logging module.
    """
    def info(self, *args):
        return self

    def warn(self, *args):
        return self

    def error(self, *args):
        return self

    def debug(self, *args):
        return self