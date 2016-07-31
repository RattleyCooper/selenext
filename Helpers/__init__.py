

class DummyLogger(object):
    def info(self, *args):
        return self

    def warn(self, *args):
        return self

    def error(self, *args):
        return self

    def debug(self, *args):
        return self