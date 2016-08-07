

class SomethingToDo(object):
    def __init__(self, some_object):
        self.some_object = some_object

    def start(self):
        print 'Starting job.'
        self.some_object.do_something('cool')

    def stop(self):
        print 'Job done.'


class SomeObject(object):
    def do_something(self, something):
        print 'SomeObject doing something {}.'.format(something)


# The start_job function is the only thing required
# for a job to be executed.
def start_job():
    # Set up objects in the start_job function.
    something_to_do = SomethingToDo(SomeObject())
    something_to_do.start()
    something_to_do.stop()
