from uuid import uuid4
import requests
from bs4 import BeautifulSoup
from lxml import etree
from .Exceptions import NoSuchElementException


class WebElement(object):
    def __init__(self, soup, response, url, parent=None):
        if soup is None:
            if response is not None:
                self.soup = BeautifulSoup(response, 'html.parser')
        else:
            self.soup = soup
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

    def clear(self, *args, **kwargs):
        # raise InteractionException('Requests WebElements do not support clearing/interacting with inputs.')
        return self

    def click(self, *args, **kwargs):
        # raise InteractionException('Requests WebElements do not support clicking.')
        return self

    def send_keys(self, *args, **kwargs):
        # raise InteractionException('Requests WebElements do not support sending keys.')
        return self

    def submit(self, *args, **kwargs):
        return self

    def screenshot(self, *args, **kwargs):
        raise AttributeError('Requests WebElements does not support screenshots.')

    def get_attribute(self, attribute, **kwargs):
        return self.soup[attribute]

    def value_of_css_property(self, name):
        return None

    def is_selected(self):
        return True

    def is_enabled(self):
        return True

    def is_displayed(self):
        return True

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

    # %%%%%%%%%%%%%%%%%%% Find elements %%%%%%%%%%%%%%%%%%%
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
        return self.history[self.index]

    def register(self, url):
        self.history.append(url)
        self.index += 1

    def back(self):
        self.index -= 1
        return self.history[self.index]

    def forward(self):
        self.index += 1
        return self.history[self.index]


class WebReader(WebElement):
    def __init__(self):
        self.soup = None
        self.current_response = None
        self.current_url = None

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

    def forward(self):
        """
        Navigate to the next place in the web history.

        Returns:
            self
        """

        self.get(self.web_history.forward())
        return self

    def get(self, url, add_to_history=True):
        """
        Get a response for the given url.

        Args:
            url:
            add_to_history:

        Returns:
            str
        """
        if add_to_history:
            self.web_history.register(url)
        self.current_url = url
        self.current_response = requests.get(url).text.strip()

        # Check for json response and if so, then return a dictionary
        # and set the current response to the dictionary.
        if self.current_response[0] == '{':
            self.current_response = self.current_response.json()
            self.soup = None
            return self.current_response

        # Make soup
        self.soup = BeautifulSoup(self.current_response, 'html.parser')

        return self.current_response
    def refresh(self):
        """
        Grab the current_url again.

        Returns:
            self
        """

        self.get(self.web_history.current_url(), add_to_history=False)
        return self
