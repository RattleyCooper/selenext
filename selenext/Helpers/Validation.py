"""
The validation module provides an api for filtering selenium elements
down using wildcard expressions, or regular expressions.

The functionality here will be expanded in the future to include
other filtering techniques.
"""
from __future__ import print_function
from re import match as rematch


# todo: Should this be kept or removed?
class WebElementFilter(object):
    def __init__(self):
        """
        The regex_special_wildcard_chars is a list of special
        regex characters, aside from `.`, and `*`.  It is
        here to help generate regex statements for any
        wildcard matching. This is done by escaping
        any character in the pattern that exists
        inside regex_special_wildcard_chars..
        """
        self._regex_special_wildcard_chars = [
            '^', '$', '+', '?', '{', '}', '[', ']', '(', ')',
            '|', ':', '<', '>', '=', '-', '!'
        ]

        self._inner_text_search = False
        self._attribute_search = False

    def _reset(self):
        """
        Reset the variables used to perform matches.

        :return:
        """

        self._inner_text_search = False
        self._attribute_search = False

    def attribute(self, attr):
        """
        Set up an attribute to match.

        :param attr:
        :return:
        """

        self._attribute_search = attr
        return self

    def inner_text(self):
        """
        Test against the inner text of an element.

        :return:
        """

        self._inner_text_search = True
        return self

    def wildcard_match(self, element, pattern, attr_name=False):
        """
        Check to see if an attribute matches a wildcard expression.

        :param element:
        :param pattern:
        :param attr_name:
        :return:
        """

        attr_value = ''

        # Handle `attribute` and `inner_text` if both are set.
        attr_search = self._attribute_search
        if attr_search and self._inner_text_search:
            self._reset()

            # Check if attribute matches.
            self.attribute(attr_search)
            if self.wildcard_match(element, pattern):
                # Don't return because we still need to check to see
                # if the inner_text matches.
                self._reset()
            else:
                self._reset()
                return False

            # Check to see if the inner text matches.
            self.inner_text()
            if self.wildcard_match(element, pattern):
                self._reset()
                # Return since both checks passed.
                return True
            else:
                self._reset()
                return False

        # Get the element attribute.
        if self._attribute_search:
            attr_value = element.get_attribute(self._attribute_search)

        # Get the elements inner text.
        if self._inner_text_search:
            attr_value = element.text

        # Get the element based on attr_name.
        if attr_name:
            attr_value = element.get_attribute(attr_name)
            # If the attribute doesn't exist, then obviously it doesn't match.
            if not attr_value:
                self._reset()
                return False

        pattern = self._prepare_wildcard_pattern(pattern)

        # Reset for reuse.
        self._reset()

        # Perform the regex match.
        if not rematch(pattern, attr_value):
            return False
        return True

    def regex_match(self, element, pattern, attr_name=False):
        """
        Check to see if an attribute matches a regular expression.

        :param element:
        :param pattern:
        :param attr_name:
        :return:
        """

        attr_value = ''

        # Handle `attribute` and `inner_text` if both are set.
        attr_search = self._attribute_search
        if attr_search and self._inner_text_search:
            self._reset()

            # Check if attribute matches.
            self.attribute(attr_search)
            if self.regex_match(element, pattern):
                # Don't return because we still need to check to see
                # if the inner_text matches.
                self._reset()
            else:
                self._reset()
                return False

            # Check to see if the inner text matches.
            self.inner_text()
            if self.regex_match(element, pattern):
                self._reset()
                # Return since both checks passed.
                return True
            else:
                self._reset()
                return False

        # Get the element attribute based on the input to the `attribute` method.
        if self._attribute_search:
            attr_value = element.get_attribute(self._attribute_search)
            print('attribute_search:', attr_value)

        # Get the elements inner text.
        if self._inner_text_search:
            attr_value = element.text

        # Get the element by attr_name kwarg.
        if attr_name:
            attr_value = element.get_attribute(attr_name)
            if not attr_value:
                return False

        # Reset for reuse.
        self._reset()

        # Perform the regex match.
        if not rematch(pattern, attr_value):
            return False
        return True

    def _prepare_wildcard_pattern(self, pat):
        """
        Prepare a regex patter for a wildcard expression. The * operator is supported.

        :param pat:
        :return:
        """

        pat = pat.replace('*', '.*')
        special_chars = self._regex_special_wildcard_chars
        return ''.join(['\\' + c if c in special_chars else c for c in pat])
