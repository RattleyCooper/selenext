"""
genesis.py is used for creating new Slack projects and writing program stubs.
"""

from __future__ import print_function

import sys
from os import mkdir
from os.path import isfile, isdir, expanduser


def write_stub(filepath, stub, append_py=True):
    """
    Write a stub to the given filepath.

    Args:
        filepath: string
        stub: string
        append_py: bool

    Returns:
        None
    """

    if append_py:
        if filepath[-3:] != '.py':
            filepath += '.py'
    with open(filepath, 'w') as f:
        f.write(stub)
        f.close()
    return


def make_threaded_stub(filepath):
    """
    Create a stub with a ThreadedCommandFactory instance for multi-threaded automations.

    Args:
        filepath: string

    Returns:
        None
    """

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
    return


def make_stub(filepath):
    """
    Create a stub for a simple automation.

    Args:
        filepath: string

    Returns:
        None
    """
    
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
    return


def make_managed_stub(filepath):
    """
    Creates a stub with a command factory instance for managing automations.

    Args:
        filepath: string

    Returns:
        None
    """

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
    return


def _get_folder(filepath):
    """
    Handles adding a / or \\ to the end of a directory path.

    Args:
        filepath: string

    Returns:
        string
    """

    if '/' in filepath:
        folder = filepath if filepath[-1] == '/' else filepath + '/'
    elif '\\' in filepath:
        folder = filepath if filepath[-1] == '\\' else filepath + '\\'
    else:
        folder = filepath + '/'
    return folder


def make_project_scaffold(directory):
    """
    Create the project scaffold in the given directory.

    Creates the .env, migrations.py, models.py and main.py files.

    Args:
        directory: string

    Returns:
        None
    """

    print()
    env_stub = """# Browsers: chrome, firefox, safari, phantomjs, opera
BROWSER=chrome

# Database settings
# DB_TYPE values: sql, mysql, postgresql, berkeley
DB_TYPE=sql
DB=default.db
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=None
DB_PASSWORD=None
"""

    migrations_stub = """from Slack.Database import migrate
import models

migrate(models)
"""
    models_stub = """from peewee import *
from Slack.Environment import get_database, env


db = get_database(env("DB_TYPE"))


class BaseModel(Model):
    class Meta:
        database = db
"""

    folder = _get_folder(directory)

    env_filename = folder + '.env'
    migrations_filename = folder + 'migrations.py'
    models_filename = folder + 'models.py'
    main_filename = folder + 'main.py'

    if not isfile(env_filename):
        print('Writing .env file...')
        write_stub(env_filename, env_stub, append_py=False)
        print('.env file written...')
    if not isfile(migrations_filename):
        print('Writing migrations.py file...')
        write_stub(migrations_filename, migrations_stub)
        print('migrations.py file written...')
    if not isfile(models_filename):
        print('Writing models.py file...')
        write_stub(models_filename, models_stub)
        print('models.py file written...')
    if not isfile(main_filename):
        print('Writing main.py file...')
        write_stub(main_filename, '')
        print('main.py file writte...')
    print()
    return


def create_module(directory):
    """
    Create a python module with the given directory path.

    Args:
        directory: string

    Returns:
        None
    """
    if not isdir(directory):
        print('Creating module folder...')
        mkdir(directory)
        print('Module folder created...')
    make_init(directory)
    return


def make_init(directory):
    """
    Create the __init__.py file.

    Args:
        directory: string

    Returns:
        None
    """
    init_filepath = directory + '__init__.py'
    if not isfile(init_filepath):
        print('Creating __init__.py...')
        write_stub(init_filepath, '')
        print('__init__.py created...')
    return None


def make_gitignore(directory):
    """
    Create the .gitignore file.
    Args:
        directory:

    Returns:
        None
    """
    gitignore_path = directory + '.gitignore'
    if not isfile(gitignore_path):
        print('Creating .gitignore...')
        write_stub(gitignore_path, '.env')
        print('.gitignore created...')
    return None


def make_project(directory):
    """
    Create a new Slack project in the given directory.

    Args:
        directory: string

    Returns:
        None
    """
    directory = expanduser(directory)
    print()
    folder = _get_folder(directory)
    site_automations_folder = _get_folder(folder + 'SiteAutomations')
    jobs_folder = _get_folder(folder + 'Jobs')

    if not isdir(folder):
        print('Creating Project: {}...'.format(folder))
        mkdir(folder)
        print('Project folder created!!!')
    else:
        print('Project folder already exists...')

    make_init(folder)
    make_gitignore(folder)

    print('Creating SiteAutomations...')
    create_module(site_automations_folder)
    print('Creating Jobs...')
    create_module(jobs_folder)
    print('Generating scaffold...')
    make_project_scaffold(directory)
    print()
    return

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

        if arg_len == 1:
            command = args[0]
        elif arg_len == 2:
            command, value = args
        elif arg_len == 3:
            command, value, the_flag = args

        if command == 'make:threaded-stub':
            make_threaded_stub(value)
        elif command == 'make:stub':
            make_stub(value)
        elif command == 'make:managed-stub':
            make_managed_stub(value)
        elif command == 'make:project':
            make_project(value)
        elif command == 'make:project_scaffold':
            make_project_scaffold(value)
        elif 'run:' in command:
            # Get the Module name
            module_name = command.split(':')[-1]
            module_obj = __import__('Project.Jobs.{}'.format(module_name), fromlist=[''])
            module_attrs = dir(module_obj)
            if 'start_job' in module_attrs:
                start_job = getattr(module_obj, 'start_job')
                start_job()
            else:
                raise AttributeError('Jobs must contain a `start_job` method.')

    main()
