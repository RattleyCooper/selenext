import sys


def write_stub(filepath, stub):
    if filepath[-3:] != '.py':
        filepath += '.py'
    with open(filepath, 'w') as f:
        f.write(stub)
        f.close()
    return True


def make_threaded_stub(filepath):
    stub = """from time import sleep
from Project import Models
from Config.Environment import env
from Helpers.Commands import ThreadedCommandFactory
from Helpers.Validation import WebElementFilter
from SiteAutomations import  # Pull in Controllers


# Replace with Controller from SiteAutomations.
controllers = {
    'controller_name': None
}
command_factory = ThreadedCommandFactory(controllers)

# Replace None with a tuple of inputs for the target method.
some_command = {
    'controller_name': None
}
# Add the target method to the call to create_command.
cmd = command_factory.create_command(, some_command)
"""
    write_stub(filepath, stub)
    return True


def make_stub(filepath):
    stub = """from time import sleep
from Project import Models
from Config.Environment import env, env_driver
from Helpers.Validation import WebElementFilter
from Helpers.Contexts import quitting
from SiteAutomations import  # Pull in Controllers


with quitting(env_driver(env("BROWSER"))()) as driver:
    pass
"""
    write_stub(filepath, stub)
    return True


def make_managed_stub(filepath):
    stub = """from time import sleep
from Project import Models
from Config.Environment import env
from Helpers.Commands import CommandFactory
from Helpers.Validation import WebElementFilter
from SiteAutomations import  # Pull in Controllers


# Replace with Controller from SiteAutomations.
controllers = {
    'controller_name': None
}
command_factory = CommandFactory(controllers)

# Replace None with a tuple of inputs for the target method.
some_command = {
    'controller_name': None
}
# Add the target method to the call to create_command.
cmd = command_factory.create_command(, some_command)
"""
    write_stub(filepath, stub)
    return True


# Start main program
if __name__ == '__main__':
    def main():
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

        if command == 'make:threaded-stub':
            make_threaded_stub(value)
        elif command == 'make:stub':
            make_stub(value)
        elif command == 'make:managed-stub':
            make_managed_stub(value)
        elif command == 'run:migrations':
            import Migrations

    main()
