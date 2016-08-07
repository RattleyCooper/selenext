

def run_job(module_name):
    module_obj = __import__('Project.Jobs.{}'.format(module_name), fromlist=[''])
    module_attrs = dir(module_obj)
    if 'start_job' in module_attrs:
        start_job = getattr(module_obj, 'start_job')
        start_job()
    else:
        print 'Jobs must contain a start_job method.'