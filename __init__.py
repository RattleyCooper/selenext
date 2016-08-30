try:
    from genesis import make_project, make_project_scaffold
except ImportError:
    pass
try:
    from .genesis import make_project, make_project_scaffold
except ImportError as err:
    raise ImportError(err)
