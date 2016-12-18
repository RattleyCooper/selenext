from __future__ import print_function


class MetaObject(object):
    """
    The purpose of this class is to create a container out of a list of objects.
    the container can run middleware on the objects

    The MetaObject takes a list of objects.  It will iterate through the list and
    assign it's own attributes key to the name of the current object in the list,
    and the value is set to the current object in the list.

    Example:

        from decimal import Decimal

        class Price(Decimal):
            name = 'price'

        class SKU(str):
            name = 'sku'

        class SubmitButton(SeleniumElement):
            name = 'submit_button'

        class Page(MetaObject):
            pass

        objects = [Price('34.99'), SKU('Some-sku-aosfij'), SubmitButton(driver.find_element_by_tag_name('button'))]
        page = Page(objects)

        print(page.sku)
        print(page.price)
        page.submit_button.click()
    """
    def __init__(self, objects):
        self._dict = {}
        self._pos = 0
        self._size = 0

        # Add objects to the MetaObject as class attributes.
        for obj in objects:
            self.add_object(obj)

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __len__(self):
        return len(self._dict)

    def __delitem__(self, key):
        del self._dict[key]

    def __iter__(self):
        return self

    def __add__(self, other):
        if isinstance(other, MetaObject):
            i1, i2 = list(self._dict.values()), list(other._dict.values())
            return MetaObject(i1 + i2)
        else:
            raise ValueError('You cannot add other object types to a MetaObject')

    @staticmethod
    def _run_middleware(obj):
        """
        Run middleware on an object.

        Args:
            obj:

        Returns:
            obj
        """

        # Check if the middleware has not been run.
        if obj.meta_run_middleware:
            # Run the middleware
            item = obj.meta_run_middleware()
            # Disable the middleware method on the object so it cannot be run again.
            setattr(item, 'meta_run_middleware', False)
            obj = item

        return obj

    @staticmethod
    def _item_name(item):
        """
        Return the item's name.  Checks for the meta_name attribute and if it can't find
        that, it uses item.__class__.__name__

        Args:
            item:

        Returns:
            str
        """
        # Figure out the objects name.
        if hasattr(item, 'meta_name'):
            return item.meta_name

        return item.__class__.__name__

    def add_object(self, obj):
        """
        Add a single object to the MetaObject

        Args:
            obj:

        Returns:
            None
        """

        # Run any middleware.
        if hasattr(obj, 'meta_run_middleware'):
            obj = MetaObject._run_middleware(obj)
            item_name = MetaObject._item_name(obj)
        else:
            item_name = MetaObject._item_name(obj)

        # Set the object as a class attribute!
        setattr(self, item_name, obj)
        # Set the internal dictionary up
        self._dict[item_name] = obj

        # Set the size so iteration works.
        self._size = len(self._dict)

    def next(self):
        """
        Allow iterating through the object.

        Returns:
            tuple
        """

        if self._pos < len(self._dict):
            keys = list(self._dict.keys())
            values = list(self._dict.values())
            k, v = keys[self._pos], values[self._pos]
            self._pos += 1
            return k, v
        raise StopIteration

    __next__ = next


class SeleniumElement(object):
    """
    The SeleniumElement object is used as a wrapper around any selenium element object.
    You can inherit from SeleniumElement to come up with new "types".  This can make
    coding go a little bit quicker because things can end up a little bit more organized.

    Example:
    Usually when you are scraping text from rows in a table there may be web elements
    associated with those rows that you need to interact with.  Creating new data types for
    the various pieces of text and the web elements allows you to just throw these things
    into a list with little regard for what order things are in later.  We can just check
    each item in the list(the row) using the `isinstance` function and deal with it how we
    want to.

    Code Example:

        # Inherit from SeleniumElement for any element you need to interact with.
        # You can also give the class a name that will show up when combined with the MetaObject
        # class.
        class RowSelector(SeleniumElement):
            name = 'selector'

        # Inherit from Decimal for the price because in this scenario it would be a pure
        # decimal number with no string characters.
        from decimal import Decimal
        class Price(Decimal):
            name = 'price'

        # Define a whole new data type for any other text data we want to scrape.
        class SKU(str):
            name = 'sku'

        # Select each column in the table and assign some new data types to the results.
        table_rows = [RowSelector(element) for element in driver.find_elements_by_id('row_selector_radio_button')]
        prices = [Price(element.text.strip()) for element in driver.find_elements_by_id('row_price')]
        skus = [SKU(element.text.strip()) for element in driver.find_elements_by_id('row_sku')]

        # Now that we have the columns in the table, we can create a list of MetaObject objects!
        # Since we have each "column" in its own list, we can use `zip` to create a list of rows!
        # Then we just use a list comprehension to change that list of rows(which are just lists
        # themselves) into a list of MetaObject objects.
        rows = [MetaObject(row) for row in zip(table_rows, prices, skus)]

        # If we iterate through the rows, you can access the various pieces we scraped
        # and even interact with any of the object if they inherited from SeleniumElement.
        for row in rows:
            if row.sku != '':
                # Click the radio button to select the row or whatever.
                print(row.price)
                print(row.sku)
                row.selector.click()
    """
    def __init__(self, element):
        self.element = element

    def __getattr__(self, item):
        if hasattr(self.element, item):
            return getattr(self.element, item)


class DummyLogger(object):
    """
    A logger that does absolutely nothing.  Meant as a drop in replacement for a
    logger that you would normally get from the logging module.
    """
    def __init__(self, prints=True, level='DEBUG'):
        self.prints = prints
        self.levels = {
            'INFO': 0,
            'DEBUG': 1,
            'WARN': 2,
            'ERROR': 3,
            'FATAL': 4
        }
        try:
            self.level = self.levels[level]
        except KeyError:
            self.level = 0

    def info(self, *args):
        if self.prints and self.level >= 0:
            print("INFO: {}".format(args))
        return self

    def debug(self, *args):
        if self.prints and self.level >= 1:
            print("DEBUG: {}".format(args))
        return self

    def warn(self, *args):
        if self.prints and self.level >= 2:
            print("WARN: {}".format(args))
        return self

    def error(self, *args):
        if self.prints and self.level >= 3:
            print("ERROR: {}".format(args))
        return self

    def fatal(self, *args):
        if self.prints and self.level >= 4:
            print("FATAL: {}".format(args))
        return self


class DummyThread(object):
    """
    A drop in for threading.Thread.  It only has the join and start methods at the moment.
    """
    def __init__(self, target=False, args=()):
        if not target:
            raise ValueError('target must be callable.')
        if len(args) == 0 or type(args) != tuple:
            raise ValueError('args must be a tuple with more than 0 values')
        self.target = target
        self.args = args

    def join(self):
        """
        Does nothing.

        :return:
        """

        pass

    def start(self):
        """
        Execute the target function with the given args.

        :return:
        """

        return self.target(*self.args)
