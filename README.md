```python
#===================================================================#
#      ___           ___       ___           ___           ___      #
#     /\  \         /\__\     /\  \         /\  \         /\__\     #
#    /::\  \       /:/  /    /::\  \       /::\  \       /:/  /     #
#   /:/\ \  \     /:/  /    /:/\:\  \     /:/\:\  \     /:/__/      #
#  _\:\~\ \  \   /:/  /    /::\~\:\  \   /:/  \:\  \   /::\__\____  #
# /\ \:\ \ \__\ /:/__/    /:/\:\ \:\__\ /:/__/ \:\__\ /:/\:::::\__\ #
# \:\ \:\ \/__/ \:\  \    \/__\:\/:/  / \:\  \  \/__/ \/_|:|~~|~    #
#  \:\ \:\__\    \:\  \        \::/  /   \:\  \          |:|  |     #
#   \:\/:/  /     \:\  \       /:/  /     \:\  \         |:|  |     #
#    \::/  /       \:\__\     /:/  /       \:\__\        |:|  |     #
#     \/__/         \/__/     \/__/         \/__/         \|__|     #
#===================================================================#
```
Slack is a micro-framework for web scraping using selenium in Python 2 or Python 3. Multi-threading is supported. This is currently still in development, however it's possible to write and run your automations within the framework as it is.

## Install

Just download this as a .zip and then unzip the `Slack` directory into 
your `site-packages` folder. Once there is a stable release, there will 
be a pip install available.

## Dependencies

For using anything that requires selenium or database interaction, you
will need:

* [peewee](http://docs.peewee-orm.com/en/latest/)
`pip install peewee` + installing peewee's dependencies.
* [selenium python bindings](http://selenium-python.readthedocs.org/)
`pip install selenium`

## Optional Dependencies

If you want to use requests to read the content off a web page using the
same API as selenium, you can use the `WebReader` class to do so.  It 
only supports reading information off of a page, so methods like `click`
are not implemented.  You'll need:

* [requests](http://docs.python-requests.org/en/master/)
`pip install requests`
* [lxml](http://lxml.de/)

`WebReader` allows you to use the `find_element`/`find_elements` methods
 to retreive `Requests.WebElement` instances.  These are different than
 a `selenium.WebElement` in the sense that interaction with the elements
 is not supported, but you can traverse the DOM and read information
 from the elements in the same way:

```python
from Slack.Helpers.Requests import WebReader

driver = WebReader()

driver.get('http://docs.python-requests.org/en/master/')
sections = driver.find_elements_by_class_name('section')
section_headers = [e.find_element_by_tag_name('h1').text for e in sections]
print(section_headers)
```

Once you have the dependencies, you can download this repository and 
start using it, however you may want to read over the documentation 
below.

## Examples

Check out [the documentation](https://github.com/Wykleph/Slack/wiki/Documentation) for the various parts and pieces in the wiki. API documentation will be coming soon.
