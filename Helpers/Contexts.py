from contextlib import contextmanager


@contextmanager
def quitting(thing):
    yield thing
    thing.close()
    thing.quit()
