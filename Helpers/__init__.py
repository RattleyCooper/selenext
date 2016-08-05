

class DummyLogger(object):
    """
    A logger that does absolutely nothing.  Meant as a drop in replacement for a
    logger that you would normally get from the logging module.
    """
    def __init__(self, prints=True):
        self.prints = prints

    def info(self, *args):
        if self.prints:
            print "INFO: {}".format(args)
        return self

    def warn(self, *args):
        if self.prints:
            print "WARN: {}".format(args)
        return self

    def error(self, *args):
        if self.prints:
            print "ERROR: {}".format(args)
        return self

    def debug(self, *args):
        if self.prints:
            print "DEBUG: {}".format(args)
        return self


class DummyThread(object):
    """
    A drop in for threading.Thread.  It only has the join and start methods at the moment.
    """
    def __init__(self, target=False, args=()):
        if not target:
            raise ValueError('target must be callable.')
        if len(args) == 0 or type(args) != tuple:
            raise ValueError('args must be a tuple with more than 0 values')
        self.target = target
        self.args = args

    def join(self):
        """
        Does nothing.

        :return:
        """

        pass

    def start(self):
        """
        Execute the target function with the given args.

        :return:
        """

        return self.target(*self.args)
