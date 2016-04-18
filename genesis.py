import sys

base_model = [
    'DoesNotExist', '__class__', '__delattr__', '__dict__', '__doc__',
    '__eq__', '__format__', '__getattribute__', '__hash__', '__init__',
    '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
    '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
    '__weakref__', '_create_indexes', '_data', '_fields_to_index',
    '_get_pk_value', '_meta', '_pk_expr', '_populate_unsaved_relations',
    '_prepare_instance', '_prune_fields', '_set_pk_value', 'alias', 'as_entity',
    'create', 'create_or_get', 'create_table', 'delete',
    'delete_instance', 'dependencies', 'dirty_fields', 'drop_table', 'filter',
    'get', 'get_id', 'get_or_create', 'id', 'insert', 'insert_from',
    'insert_many', 'is_dirty', 'prepared', 'raw', 'save', 'select',
    'set_id', 'sqlall', 'table_exists', 'update'
]


def _get_methods(name):
    return """
    def set_{}(self, value):
        return value

    def get_{}(self, value):
        return value
""".format(name, name)


def _get_middleware(name, methods):
    """ Create the string for the Middleware class being generated. """

    return '''from Middleware import Middleware


class {}Middleware(Middleware):
    """ Middleware for the {} Model. """
{}
'''.format(name, name, methods)


def make_model(name, flag=None):
    """ Handles the make:model command. """

    model_template = """

class {}(BaseModel):

    created_at = DateTimeField(default=datetime.datetime.now)
""".format(name)
    with open('Models.py', 'a') as f:
        f.write(model_template)
        f.close()

    print 'created `{}` model in Models.py...'.format(name)

    flag = flag.lower()

    if flag == '--no-middleware' or flag == '-no-middleware':
        return True

    make_middleware(name)

    return True


def make_middleware(name):
    """ Handles the make:middleware command. """

    import Models

    if name not in dir(Models):
        print 'Model does not exist. Run make:model {}'.format(name)
        return

    module = getattr(Models, name)
    module_parts = dir(module)
    methods = ''
    for part in module_parts:
        if part not in base_model:
            methods += _get_methods(part)

    with open('Middleware/{}Middleware.py'.format(name), 'w') as f:
        f.write(_get_middleware(name, methods))
        f.close()
    print 'created `{}Middleware` in `Middleware/{}Middleware.py`...'.format(name, name)
    return True

# Start main program
if __name__ == '__main__':
    args = sys.argv[1:]

    arg_len = len(args)

    if arg_len >= 4:
        exit()

    command = None
    value = None
    the_flag = None

    if arg_len == 2:
        command, value = args
    elif arg_len == 3:
        command, value, the_flag = args

    if command == 'make:model':
        make_model(value, the_flag)
    elif command == 'make:middleware':
        """ Expects a model name. """
        make_middleware(value)
    elif command == 'run:migrations':
        import Migrations
