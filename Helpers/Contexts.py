from contextlib import contextmanager


@contextmanager
def quitting(thing):
    yield thing
    thing.close()
    try:
        thing.quit()
    except AttributeError:
        pass
