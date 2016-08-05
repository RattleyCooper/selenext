

class DummyLogger(object):
    """
    A logger that does absolutely nothing.  Meant as a drop in replacement for a
    logger that you would normally get from the logging module.
    """
    def __init__(self, prints=True, level='DEBUG'):
        self.prints = prints
        self.levels = {
            'INFO': 0,
            'DEBUG': 1,
            'WARN': 2,
            'ERROR': 3,
            'FATAL': 4
        }
        try:
            self.level = self.levels[level]
        except KeyError:
            self.level = 0

    def info(self, *args):
        if self.prints and self.level >= 0:
            print "INFO: {}".format(args)
        return self

    def debug(self, *args):
        if self.prints and self.level >= 1:
            print "DEBUG: {}".format(args)
        return self

    def warn(self, *args):
        if self.prints and self.level >= 2:
            print "WARN: {}".format(args)
        return self

    def error(self, *args):
        if self.prints and self.level >= 3:
            print "ERROR: {}".format(args)
        return self

    def fatal(self, *args):
        if self.prints and self.level >= 4:
            print "FATAL: {}".format(args)
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
