import sys


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
    elif command == 'run:migrations':
        import Migrations
