from os import getcwd


__SLACK_FRAMEWORK_ENV_PATH = getcwd()\
                                 .replace('\\', '/')\
                                 .replace('SiteAutomations', '')\
                                 .replace('Jobs', '')

__SLACK_FRAMEWORK_ENV_PATH += '/.env' if __SLACK_FRAMEWORK_ENV_PATH[-1] != '/' else '.env'


class ConfigLoader:
    def __init__(self, filepath='.env'):
        self.lines = {}
        self.list_mode = False
        self.list_name = None
        self.dict_mode = False
        self.dict_name = None
        self.sline = None
        with open(filepath, 'r') as f:

            for line in f:
                self.sline = line.strip()

                # Handle comments.
                if line[0] == '#':
                    continue

                # Handle dict mode.
                if self.dict_mode:
                    if self.sline == self.dict_name + '{END}':
                        if self.dict_name not in self.lines.keys():
                            self.lines[self.dict_name] = {}
                        self.dict_mode = False
                        self.dict_name = None
                        continue

                    self.process_dict_line(line, self.dict_name)
                    continue

                # Handle list mode.
                if self.list_mode:
                    if self.sline == '{}[END]'.format(self.list_name):
                        if self.list_name not in self.lines.keys():
                            self.lines[self.list_name] = []
                        self.list_name = None
                        self.list_mode = False
                        continue
                    try:
                        self.lines[self.list_name].append(self.sline)
                    except KeyError:
                        self.lines[self.list_name] = [self.sline]
                    continue

                # Handle key=value lines.
                if '=' in line:
                    self.process_key_value(line)
                    continue

                # Handle list definitions.
                if self.sline[-3:] == '[]:':
                    self.list_mode = True
                    self.list_name = self.sline[:-3]
                    continue

                # Handle dict definitions.
                if self.sline[-3:] == '{}:':
                    self.dict_mode = True
                    self.dict_name = self.sline[:-3]
                    continue

    def check_for_list_mode(self, line):
        """
        Check to see if the line is defining a list or not.  If it does, it will return
        the lists name and the bool representing whether it is in list mode or not.

        Args:
            line:

        Returns:
            tuple
        """

        self.list_name = self.sline[:-3]
        self.list_mode = True if self.sline[-3:] == '[]:' else False
        return self.list_name, self.list_mode

    def check_for_dict_mode(self, line):
        """
        Check to see if the line is defining a dictionary or not.  If it does, it will return
        the dictionaries name and the bool representing whether it is in dict mode or not.

        Args:
            line:

        Returns:
            tuple
        """

        self.dict_name = self.sline[:-3]
        self.dict_mode = True if self.sline[-3:] == '{}:' else False
        return self.dict_name, self.dict_mode

    def get_key_value(self, line):
        """
        Get the key and value from the given line, assuming it's separated by the first = sign.

        Args:
            line:

        Returns:

        """

        line_pieces = self.sline.split('=')
        key = line_pieces[0]
        # Safely grab the value.  If the value contains an = symbol, it should
        # not get mangled, and data should not be missing
        value = '='.join(line_pieces[1:]).strip()

        return key, value

    def process_dict_line(self, line, dict_name):
        """
        Process a line that occurs within a dict that is being defined in the .env file.

        Args:
            line:
            dict_name:

        Returns:
            self
        """

        key, value = self.get_key_value(line)
        try:
            self.lines[dict_name][key] = value
        except KeyError:
            self.lines[dict_name] = {key: value}
        return self

    def process_key_value(self, line):
        """
        Process a key=value from the given line.

        Args:
            line:

        Returns:
            self
        """

        key, value = self.get_key_value(line)
        self.add_root_key(key, value)
        return self

    def add_root_key(self, key, value):
        """
        Add a key to self.lines with the given value.

        Args:
            key:
            value:

        Returns:
            self
        """

        self.lines[key] = value
        return self

    def get(self, variable_name):
        """

        Args:
            variable_name: string

        Returns:
            string
        """

        return self.lines[variable_name]

# We use a global variable for the resource loader so that we are not constantly opening
# the same file.  This will hold the config file in the ConfigLoader object so that
# reloading is only done on imports.
__SLACK_FRAMEWORK_RESOURCE_LOADER = ConfigLoader(filepath=__SLACK_FRAMEWORK_ENV_PATH)


def env(variable_name, func=lambda x: x if x else x):
    """
    Get the corresponding environment variable.  Pass a function
    like `int` or `bool` as the `type_hint` keyword argument to
    automatically run that function on the output.

    Args:
        variable_name: string
        func: function

    Returns:
        string
    """

    return func(__SLACK_FRAMEWORK_RESOURCE_LOADER.get(variable_name))


def env_driver(browser):
    """
    Return the web driver.

    Args:
        browser: string

    Returns:
        selenium WebDriver
    """

    from selenium import webdriver

    the_driver = False
    if browser == 'chrome':
        the_driver = webdriver.Chrome

    elif browser == 'firefox':
        the_driver = webdriver.Firefox

    elif browser == 'safari':
        the_driver = webdriver.Safari

    elif browser == 'phantomjs':
        the_driver = webdriver.PhantomJS

    elif browser == 'opera':
        the_driver = webdriver.Opera

    return the_driver


def get_database(db_type):
    """
    Get the database object that should be used.

    Args:
        db_type: string

    Returns:
        peewee database driver.
    """

    db = False
    if db_type == 'sql':
        from peewee import SqliteDatabase

        db = SqliteDatabase(env("DB"))

    elif db_type == 'mysql':
        from peewee import MySQLDatabase

        db = MySQLDatabase(
            env("DB"),
            host=env("DB_HOST"),
            port=int(env("DB_PORT")),
            user=env("DB_USERNAME"),
            passwd=env("DB_PASSWORD")
        )

    elif db_type == 'postgresql':
        from peewee import PostgresqlDatabase

        db = PostgresqlDatabase(
            env('DB'),
            host=env("DB_HOST"),
            port=int(env("DB_PORT")),
            user=env("DB_USERNAME"),
            passwd=env("DB_PASSWORD")
        )

    elif db_type == 'berkeley':
        from playhouse.berkeleydb import BerkeleyDatabase

        db = BerkeleyDatabase(
            env('DB'),
            host=env("DB_HOST"),
            port=int(env("DB_PORT")),
            user=env("DB_USERNAME"),
            passwd=env("DB_PASSWORD")
        )

    return db
