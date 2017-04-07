

class EnvironmentContainer(object):
    """
    Static container object used to facilitate holding environment variables across
    instances.
    """

    container = {}

    def __getattribute__(self, item):
        if item == 'container':
            return object.__getattribute__(self, 'container')

        try:
            return object.__getattribute__(self, 'container')[item]
        except KeyError:
            return object.__getattribute__(self, item)

    def __getitem__(self, item):
        container = object.__getattribute__(self, 'container')
        return container[item]

    def __setattr__(self, key, value):
        if key == 'container':
            object.__setattr__(self, key, value)
            return
        container = object.__getattribute__(self, 'container')
        container[key] = value
        return self

    def __setitem__(self, key, value):
        container = object.__getattribute__(self, 'container')
        container[key] = value
        return self

    def __call__(self, *args, **kwargs):
        # Set value in container if there are 2 args
        if len(args) == 2:
            self.container[args[0]] = args[1]
            return self

        # Retrieve a value for the given arg if 1 arg.
        container = object.__getattribute__(self, 'container')
        return container[args[0]]


class ConfigParser:
    def __init__(self, filepath='.env'):
        self.filepath = filepath
        self.lines = {}
        self.list_mode = False
        self.list_name = None
        self.dict_mode = False
        self.dict_name = None
        self.sline = None
        self.container = EnvironmentContainer()

    def load(self):
        filepath = self.filepath
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
        for k, v in self.lines.items():
            self.container[k] = v

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


