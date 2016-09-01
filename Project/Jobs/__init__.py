

def run_job(module_name, *args, **kwargs):
    """
    Run a job by name.

    :param module_name:
    :param args:
    :return:
    """

    module_obj = __import__('Jobs.{}'.format(module_name), fromlist=[''])
    module_attrs = dir(module_obj)

    if 'start_job' in module_attrs:
        start_job = getattr(module_obj, 'start_job')
        if args and kwargs:
            start_job(*args, **kwargs)
        elif args:
            start_job(*args)
        elif kwargs:
            start_job(**kwargs)
        else:
            start_job()
    else:
        raise AttributeError('Jobs must contain a `start_job` method.')
