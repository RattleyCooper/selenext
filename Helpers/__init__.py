from __future__ import print_function
from time import sleep
from json import loads
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class PageState(object):
    """
    Object for holding the definition of a web page's state, waiting for the state,
    and checking to see if the web page is in the defined state.
    """
    def __init__(self, driver, elements, state_dict):
        self._driver = driver
        self._elements = elements
        self._state_dict = state_dict

    def __call__(self, *args, **kwargs):
        """
        Return True if the page matches the given state and False if not.

        :param args:
        :param kwargs:
        :return: bool
        """

        for aen in self._pull_from_dict(self._state_dict, 'exists'):
            if not self._get_page_element(aen).exists():
                return False

        for den in self._pull_from_dict(self._state_dict, 'absent'):
            if self._get_page_element(den).exists():
                return False

        for nden in self._pull_from_dict(self._state_dict, 'not_displayed'):
            nden_page_element = self._get_page_element(nden)
            if not nden_page_element.exists():
                return False
            if nden_page_element.exists() and nden_page_element.is_displayed():
                return False

        for disen in self._pull_from_dict(self._state_dict, 'displayed'):
            disen_page_element = self._get_page_element(disen)
            disen_exists = disen_page_element.exists()
            if not disen_exists:
                return False
            elif disen_exists and not disen_page_element().is_displayed():
                return False

        for enabled_en in self._pull_from_dict(self._state_dict, 'enabled'):
            enabled_page_element = self._get_page_element(enabled_en)
            enabled_exists = enabled_page_element.exists()
            if not enabled_exists:
                return False
            elif enabled_exists and not enabled_page_element().is_enabled():
                return False

        for enabled_en in self._pull_from_dict(self._state_dict, 'disabled'):
            enabled_page_element = self._get_page_element(enabled_en)
            enabled_exists = enabled_page_element.exists()
            if not enabled_exists:
                return False
            elif enabled_exists and enabled_page_element().is_enabled():
                return False

        return True

    def wait(self, timeout=30):
        """
        Wait for the conditions set in the state dict to be met.

        Args:
            timeout:

        Returns:
            self
        """

        page_settings = self._state_dict

        exists = self._pull_from_dict(page_settings, 'exists')
        absent = self._pull_from_dict(page_settings, 'absent')
        not_displayed = self._pull_from_dict(page_settings, 'not_displayed')
        displayed = self._pull_from_dict(page_settings, 'displayed')
        enabled = self._pull_from_dict(page_settings, 'enabled')
        disabled = self._pull_from_dict(page_settings, 'disabled')

        for appears_element_name in exists:
            self._get_page_element(appears_element_name).wait_exists(timeout=timeout)

        for displayed_element_name in displayed:
            self._get_page_element(displayed_element_name).wait_displayed(timeout=timeout)

        for enabled_element_name in enabled:
            self._get_page_element(enabled_element_name).wait_enabled(timeout=timeout)

        for disabled_element_name in disabled:
            self._get_page_element(disabled_element_name).wait_disabled(timeout=timeout)

        for not_displayed_element_name in not_displayed:
            self._get_page_element(not_displayed_element_name).wait_not_displayed(timeout=timeout)

        for disappear_element_name in absent:
            self._get_page_element(disappear_element_name).wait_absent(timeout=timeout)

        return self

    def _pull_from_dict(self, settings, name):
        try:
            return settings[name]
        except KeyError:
            return []

    def _get_page_element(self, name):
        """
        Get a PageElement from the datastore using the given name.
        Args:
            name:

        Returns:

        """
        ele = self._elements[name]
        if isinstance(ele, PageElement):
            output_element = self._elements[name]
        else:
            output_element = PageElement(self._driver, ele)

        return output_element


class PageStateContainer(object):
    """
    Container for holding PageState objects and allowing dynamic access to them as attributes.
    """
    def __init__(self, driver, elements, state_dict):
        self._driver = driver
        self._elements = elements
        self._state_dict = state_dict
        self._handle_state_dict(state_dict)

    def _handle_state_dict(self, state_dict):
        """
        Handle the definition of the web page states by setting up the _states attributes and
        dynamically setting up the rest of the attributes in the dictionary.

        Args:
            state_dict:

        Returns:

        """
        try:
            state_dict_iterator = state_dict.iteritems()
        except AttributeError:
            state_dict_iterator = state_dict.items()

        self._states = {}

        for page_name, settings in state_dict_iterator:
            self._states[page_name] = PageState(self._driver, self._elements, settings)
            setattr(self, page_name, self._states[page_name])

        return self

    def wait(self, state_name, timeout=30):
        """
        Wait for the web page to be in the defined state(by state_name). Only invoke this
        method when you expect the web page to be in that current state.

        Args:
            state_name:
            timeout:

        Returns:
            self
        """

        state = getattr(self, state_name)
        state.wait(timeout=timeout)

        return self


class PageElement(object):
    """
    The PageElement object holds a selenium WebDriver instance and directions on how to
    find a given element on the page.  When an instance of the PageElement object has
    it's __call__ method invoked it will use the WebDriver instance to look up and
    return the WebElement it finds.  If the element cannot be found, it will raise
    the same selenium error.
    """
    def __init__(self, driver, element_dict):
        self.driver = driver
        self.element_dict = element_dict
        self.parent = None

        try:
            bind_path = element_dict['bind']
        except KeyError:
            bind_path = False

        # Handle any binds.
        if bind_path:
            new_func = self._get_bind(bind_path)
            # Set the bind to the object we pulled in, instead of the string that locates the object.
            element_dict['bind'] = new_func

        try:
            frame_location = element_dict['frame']
        except KeyError:
            frame_location = False

        if frame_location:
            frame_location = self._handle_frame(frame_location)
            element_dict['frame'] = frame_location

        # Set up the parent element
        try:
            parent_location = element_dict['parent']
        except KeyError:
            parent_location = False

        if parent_location:
            parent_location = self._handle_parent(parent_location)
            element_dict['parent'] = parent_location

        self._handle_element_dict(element_dict)

    def _handle_parent(self, parent_location):
        """
        Return a parent element based on teh parent location dictionary.

        Args:
            parent_location:

        Returns:
            ParentElement
        """

        return ParentElement(self.driver, parent_location)

    def __call__(self, *args, **kwargs):
        """
        Lookup the WebElement using the WebDriver.  It will navigate parent elements
        and even frames.  Frames can even be selected using parent elements(in the
        JSON).

        Args:
            *args:
            **kwargs:

        Returns:
            WebElement
        """

        if not isinstance(self, Frame):
            self.driver.switch_to_default_content()

        if hasattr(self, 'frame'):
            frame = getattr(self, 'frame')
            self.driver.switch_to.frame(frame())

        lookup_method = self._get_lookup_method()

        output = lookup_method(getattr(self, 'selector'))
        # Since parents are used to locate elements, we
        # don't need to worry about any bindings.
        if isinstance(self, ParentElement):
            return output

        # Bind the text if needed.
        if hasattr(self, 'bind'):
            binding = getattr(self, 'bind')
            if type(output) == list:
                output = [binding(t.text) for t in output]
            else:
                output = binding(output.text)
        return output

    def exists(self):
        """
        Return true if the element exists.

        Returns:
            bool
        """

        try:
            lookup_method = self._get_lookup_method()
            ele = lookup_method(getattr(self, 'selector'))
            if ele:
                return True
            return False
        except NoSuchElementException:
            return False

    def wait_disabled(self, timeout=30):
        """
        Wait for the element to be disabled.

        Args:
            timeout: None or int

        Returns:
            self
        """

        wait_time = 0

        web_element = self()
        while web_element.is_enabled():
            sleep(1)
            wait_time += 1
            if timeout is not None:
                if wait_time >= timeout:
                    raise TimeoutException()
        return self

    def wait_enabled(self, timeout=30):
        """
        Wait for the element to be enabled.

        Args:
            timeout: None or int

        Returns:
            self
        """

        wait_time = 0

        web_element = self()
        while not web_element.is_enabled():
            sleep(1)
            wait_time += 1
            if timeout is not None:
                if wait_time >= timeout:
                    raise TimeoutException()
        return self

    def wait_not_displayed(self, timeout=30):
        """
        Wait for the element to not be displayed any longer.

        Args:
            timeout: None or int

        Returns:
            self
        """

        wait_time = 0

        while self().is_displayed():
            sleep(1)
            wait_time += 1
            if timeout is not None:
                if wait_time >= timeout:
                    raise TimeoutException()
        return self

    def wait_displayed(self, timeout=None):
        """
        Wait for the element to be displayed.

        Args:
            timeout: None or int

        Returns:
            self
        """

        wait_time = 0

        while not self().is_displayed():
            sleep(1)
            wait_time += 1
            if timeout is not None:
                if wait_time >= timeout:
                    raise TimeoutException()
        return self

    def wait_exists(self, timeout=None):
        """
        Wait for the element to appear in the DOM.

        Args:
            timeout: None or int

        Returns:
            self
        """

        wait_time = 0
        while not self.exists():
            sleep(1)
            wait_time += 1
            if timeout is not None:
                if wait_time >= timeout:
                    raise TimeoutException()
        return self

    def wait_absent(self, timeout=None):
        """
        Wait for the element to no longer appear in the DOM.

        Args:
            timeout: None or int

        Returns:
            self
        """

        wait_time = 0
        while self.exists():
            sleep(1)
            wait_time += 1
            if timeout is not None:
                if wait_time >= timeout:
                    raise TimeoutException()
        return self

    def _handle_element_dict(self, element_dict):
        """
        Set attributes based on the given dict.

        Args:
            element_dict:

        Returns:
            self
        """

        try:
            iterable = element_dict.iteritems()
        except AttributeError:
            iterable = element_dict.items()

        for k, v in iterable:
            setattr(self, k, v)

        return self

    def _get_lookup_method(self):
        """
        Return the method used for looking up the element.

        Returns:
            WebDriver method
        """

        if self.parent is not None:
            parent = getattr(self, 'parent')()
        else:
            parent = self.driver
        # Handle finding multiple elements
        if hasattr(self, 'multiple'):
            lookup_method = getattr(parent, 'find_elements_by_{}'.format(getattr(self, 'lookup_method')))
        else:
            lookup_method = getattr(parent, 'find_element_by_{}'.format(getattr(self, 'lookup_method')))

        return lookup_method

    def _get_bind(self, bind_path):
        """
        Get the callable object based on the bind path given.

        Args:
            bind_path:

        Returns:
            callable
        """

        # Handle direct imports
        if type(bind_path) == list:
            imp, obj = bind_path
            p = __import__(imp, fromlist=[''])
            new_func = getattr(p, obj)
        # Check if the bind_path exists in the builtins and use that if it does.
        elif bind_path in __builtins__:
            new_func = __builtins__[bind_path]
        # Check to see if it's drilling into a module function or class.
        elif '.' in bind_path:
            steps = bind_path.split('.')
            new_func = __import__(steps[0], fromlist=[''])
            for step in steps[1:]:
                new_func = getattr(new_func, step)
        # If none of those things apply then try a regular import
        else:
            try:
                new_func = __import__(bind_path, fromlist=[''])
            except ImportError:
                raise ImportError('Could not find the object to bind to: {}'.format(bind_path))

        return new_func

    def _handle_frame(self, frame_location):
        """
        Return a Frame instance based on the given frame location.

        Args:
            frame_location:

        Returns:
            Frame
        """

        return Frame(self.driver, frame_location)


class ParentElement(PageElement):
    """
    Needed so the PageElement object knows to handle these instances differently.
    """
    pass


class Frame(PageElement):
    """
    Needed so the PageElement object knows to handle these instances differently.
    """
    pass


class View(object):
    """
    The View object is a container for view/page's JSON definition.  It sets up
    everything so that the page object can access what it needs.
    """
    def __init__(self, driver, json, file=False):
        self.driver = driver

        if file:
            with open(json, 'r') as f:
                json = f.read().strip()

        if type(json) == str:
            json = loads(json)

        self.json_dict = json
        self._handle_view_dict(json)

    def get(self, item):
        """
        Wrapper around WebDriver().get()

        Args:
            item:

        Returns:

        """

        return self.driver.get(item)

    def __getattribute__(self, item):
        thing = object.__getattribute__(self, item)
        # if isinstance(thing, PageElement):
        #     return thing()
        return thing

    def _handle_view_dict(self, json_dict):
        """
        Handle the elements in the view dict.  Set attributes and handle all the
        special attributes in the dict.

        Args:
            json_dict:

        Returns:
            self
        """
        try:
            iterable = json_dict.iteritems()
        except AttributeError:
            iterable = json_dict.items()

        for k, v in iterable:
            if k == 'elements':
                self._handle_elements(v)
            if k == 'states':
                k = '_states'
            setattr(self, k, v)

        if hasattr(self, 'elements') and hasattr(self, '_states'):
            self.state = PageStateContainer(self.driver, self.elements, self._states)

        return self

    def _handle_elements(self, element_dict):
        """
        Set up the elements dictionary along with the element attributes.

        Args:
            element_dict:

        Returns:
            self
        """

        try:
            element_dict_iterator = element_dict.iteritems()
        except AttributeError:
            element_dict_iterator = element_dict.items()

        self.elements = {}

        for element_name, the_dict in element_dict_iterator:
            # Set the element up in the dict.
            self.elements[element_name] = PageElement(self.driver, the_dict)
            setattr(self, element_name, self.elements[element_name])

        return self


class Page(object):
    """
    The Page object is a light wrapper around the View object.  They are almost the same
    but the Page object makes accessing elements on the page a bit simpler.
    """
    def __init__(self, driver, json, file=False):
        self.driver = driver
        self.view = View(driver, json, file=file)

    def __bool__(self):
        try:
            iterable = self.view.elements.iteritems()
        except AttributeError:
            iterable = self.view.elements.items()

        for k, v in iterable:
            test_element = getattr(self.view, k)
            if not test_element.exists():
                return False

        return True

    def __getattr__(self, item):
        # Check if the page_view has the item.
        if hasattr(self.view, item):
            # Handle PageElements by calling the instance and getting the
            # actual selenium web element.
            if isinstance(getattr(self.view, item), PageElement):
                return getattr(self.view, item)()
            # Handle any other items.
            return getattr(self.view, item)

        raise AttributeError()


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
