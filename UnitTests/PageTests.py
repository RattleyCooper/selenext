from __future__ import print_function
import unittest

from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenext.Helpers import Page, View, PageElement, ParentElement
from json.decoder import JSONDecodeError


class PageTest(unittest.TestCase):
    def setUp(self):
        self.driver = Chrome()
        self.assertIsInstance(self.driver, WebDriver)

        self.page = Page(self.driver, 'test_case_page.json', file=True)

    def test_page_instance_is_page(self):
        self.assertIsInstance(self.page, Page)

    def test_page_instantiation(self):
        self.assertRaises(TypeError, Page)
        self.assertRaises(TypeError, Page, self.driver)
        self.assertRaises(JSONDecodeError, Page, self.driver, '')
        self.assertRaises(JSONDecodeError, Page, self.driver, 'test_case_page.json')

    def test_page_attributes(self):
        self.assertIsInstance(self.page.driver, WebDriver)
        self.assertIsInstance(self.page.root, str)
        self.page.get(self.page.root)
        # In the debugger, the self.page.search_input attribute equals a PageElement,
        # but as soon as the attribute is accessed, it will change to a WebElement.
        self.assertIsInstance(self.page.search_input, WebElement)
        self.assertIsInstance(self.page.view.search_input, PageElement)

    def test_page_view_attributes(self):
        self.assertIsInstance(self.page.view, View)
        self.assertIsInstance(self.page.view.elements, dict)
        self.assertIsInstance(self.page.view.json_dict, dict)
        self.assertIsInstance(self.page.view.driver, WebDriver)

    def test_page_element_attributes(self):
        self.assertIsInstance(self.page.view.search_input.driver, WebDriver)
        self.assertIsInstance(self.page.view.search_input.element_dict, dict)
        self.assertIsInstance(self.page.view.search_input.lookup_method, str)
        self.assertIsInstance(self.page.view.search_input.selector, str)
        self.assertIsInstance(self.page.view.search_input, PageElement)
        self.assertIsInstance(self.page.view.search_form.parent, ParentElement)
        self.assertIsInstance(self.page.view.search_form.parent.parent, ParentElement)
        self.assertIsInstance(self.page.view.search_input.parent, None)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
