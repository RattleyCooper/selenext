from contextlib import contextmanager


@contextmanager
def quitting(thing):
    """
    Calls close() and quit() on thing.

    :param thing:
    :return:
    """

    yield thing
    thing.close()
    try:
        thing.quit()
    except AttributeError:
        pass
