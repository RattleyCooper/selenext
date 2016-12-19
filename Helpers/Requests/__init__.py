from uuid import uuid4
import requests
from bs4 import BeautifulSoup
from lxml import etree
from json import loads
from .Exceptions import NoSuchElementException


class WebElement(object):
    """
    The Requests WebElement behaves very much like a selenium WebElement
    except that it does not provide any methods for interaction like
    clicking and sending keys.  DOM Traversal and data extraction
    methods are provided, and attributes like WebElement.text
    are available.
    """
    def __init__(self, soup, response, url, parent=None):

        self.soup = None
        self.make_soup(soup, response)

        self.tag_name = self.soup.name if self.soup is not None else None
        self.text = self.soup.text if self.soup is not None else None
        try:
            self.content = self.soup.content if self.soup is not None else None
        except AttributeError:
            self.content = None
        self.current_response = response
        self.current_url = url
        self.size = 0, 0
        self.location = 0, 0
        self.rect = 0, 0
        self.screenshot_as_png = None
        self.screenshot_as_base64 = None
        self.parent = parent
        self.location_once_scrolled_into_view = 0, 0
        self.id = uuid4()

    def __getitem__(self, item):
        return self.soup[item]

    def make_soup(self, soup, response):
        if soup is None:
            if response is not None:
                soup = BeautifulSoup(response, 'html.parser')
                tag = None
                for thing in soup.children:
                    tag = getattr(soup, thing.name)
                    # If we don't have a valid tag object, then continue looking.
                    if not tag or tag is None:
                        continue
                    break

                self.soup = tag
        else:
            self.soup = soup

        return self

    def get_attribute(self, attribute, **kwargs):
        return self.soup[attribute]

    def value_of_css_property(self, name):
        return None

    def find_element_by_id(self, element_id):
        ele = self.soup.find(id=element_id)
        if ele is None:
            raise NoSuchElementException('The element could not be located by id: {}'.format(element_id))

        return WebElement(ele, self.current_response, self.current_url, parent=self.id)

    def find_element_by_name(self, name):
        ele = self.soup.find(attrs={'name': name})
        if ele is None:
            raise NoSuchElementException('The element could not be located by name: {}'.format(name))

        return WebElement(ele, self.current_response, self.current_url, parent=self.id)

    def find_element_by_class_name(self, class_name):
        ele = self.soup.find(attrs={'class': class_name})
        if ele is None:
            raise NoSuchElementException('The element could not be located by class name: {}'.format(class_name))

        return WebElement(ele, self.current_response, self.current_url, parent=self.id)

    def find_element_by_tag_name(self, tag_name):
        ele = self.soup.find(tag_name)
        if ele is None:
            raise NoSuchElementException('The element could not be located by tag name: {}'.format(tag_name))

        return WebElement(ele, self.current_response, self.current_url, parent=self.id)

    def find_element_by_css_selector(self, selector):
        ele = self.soup.select(selector)[0]
        if ele is None:
            raise NoSuchElementException('The element could not be located by css selector: {}'.format(selector))

        return WebElement(ele, self.current_response, self.current_url, parent=self.id)

    def find_element_by_xpath(self, xpath):
        tree = etree.fromstring(self.current_response, etree.HTMLParser())
        element = tree.xpath(xpath)[0]
        self.current_response = etree.tostring(element)
        print(self.current_response)
        return WebElement(None, self.current_response, self.current_url, parent=self.id)

    # %%%%%%%%%%%%%%%%%%% Find elements %%%%%%%%%%%%%%%%%%% #
    def find_elements_by_id(self, element_id):
        resp = self.current_response
        url = self.current_url
        return [WebElement(element, resp, url, parent=self.id) for element in self.soup.find_all(id=element_id)]

    def find_elements_by_name(self, name):
        resp = self.current_response
        url = self.current_url
        return [WebElement(element, resp, url, parent=self.id) for element in self.soup.find_all(attrs={'name': name})]

    def find_elements_by_class_name(self, name):
        resp = self.current_response
        url = self.current_url
        return [WebElement(element, resp, url, parent=self.id) for element in self.soup.find_all(attrs={'class': name})]

    def find_elements_by_tag_name(self, name):
        resp = self.current_response
        url = self.current_url
        return [WebElement(element, resp, url, parent=self.id) for element in self.soup.find_all(name)]

    def find_elements_by_css_selector(self, selector):
        resp = self.current_response
        url = self.current_url
        return [WebElement(element, resp, url, parent=self.id) for element in self.soup.select(selector)]

    def find_elements_by_xpath(self, xpath):
        tree = etree.fromstring(self.current_response, etree.HTMLParser())
        elements = tree.xpath(xpath)

        output_elements = []
        for element in elements:
            resp = etree.tostring(element)
            output_elements.append(WebElement(None, resp, self.current_url, parent=self.id))

        return output_elements


class WebHistory(object):
    def __init__(self):
        self.index = -1
        self.history = []

    def __getitem__(self, item):
        return self.history[item]

    def current_url(self):
        """
        Get the current index's url.

        Returns:
            str
        """

        return self.history[self.index]

    def register(self, url):
        """
        Register a url with the history list.

        Args:
            url:
                str
        Returns:
            self
        """

        self.history.append(url)
        self.index += 1
        return self

    def back(self):
        """
        Move the pointer back in the history and return the url for that new index.

        Returns:
            str
        """

        self.index -= 1
        return self.history[self.index]

    def forward(self):
        """
        Move the pointer forward in the history and return the url for that new index.

        Returns:
            str
        """

        self.index += 1
        return self.history[self.index]


class WebReader(WebElement):
    def __init__(self):
        self.soup = None
        self.current_response = None
        self.current_url = None

        self.requests = requests
        self.web_history = WebHistory()

        self.size = 0, 0
        self.location = 0, 0
        self.rect = 0, 0
        self.screenshot_as_png = None
        self.screenshot_as_base64 = None
        self.location_once_scrolled_into_view = 0, 0
        self.id = uuid4()

        super(WebReader, self).__init__(None, None, None)

    def back(self):
        """
        Navigate to the last place in the web history.

        Returns:
            self
        """

        self.get(self.web_history.back())
        return self

    def close(self):
        """
        Does nothing.  Is just a placeholder method.

        Returns:
            self
        """

        return self

    def forward(self):
        """
        Navigate to the next place in the web history.

        Returns:
            self
        """

        self.get(self.web_history.forward())
        return self

    def get(self, url, headers=None, add_to_history=True):
        """
        Get a response for the given url.

        Args:
            url:
            headers:
            add_to_history:

        Returns:
            str
        """

        if add_to_history:
            self.web_history.register(url)
        self.current_url = url

        if headers is None:
            headers = {}

        self.current_response = self.requests.get(url, headers=headers).text.strip()

        # Check for json response and if so, then return a dictionary
        # and set the current response to the dictionary.
        if self.current_response[0] == '{':
            if hasattr(self.current_response, 'json'):
                self.current_response = self.current_response.json()
            self.current_response = loads(self.current_response)
            self.soup = None
            return self.current_response

        # Make soup
        self.soup = BeautifulSoup(self.current_response, 'html.parser')

        return self.current_response

    def quit(self):
        """
        Does nothing.  Is just a placeholder method.

        Returns:
            self
        """

        return self

    def refresh(self):
        """
        Grab the current_url again.

        Returns:
            self
        """

        self.get(self.web_history.current_url(), add_to_history=False)
        return self
