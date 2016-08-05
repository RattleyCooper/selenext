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
Slack is a micro-framework for web scraping using selenium.  Multi-threading is supported.

## Install

Just download this as a .zip and then open it as a project in an IDE like PyCharm.

## Dependencies

* [peewee](http://docs.peewee-orm.com/en/latest/)
`pip install peewee` + installing peewee's dependencies.
* [selenium python bindings](http://selenium-python.readthedocs.org/)
`pip install selenium`

Once you have the dependencies, you can download this repository and start using it as is, however you may want to read over the
documentation below.

## Examples

_There is an [`Example.py`](https://github.com/Wykleph/Slack/blob/master/Example.py) file that shows what the master controller of an application looks like when utilizing the `Slack`
framework.  `Example.py` can be used as a template.  There is also a [`ThreadedExample.py`](https://github.com/Wykleph/Slack/blob/master/ThreadedExample.py) file that shows how to
create a multithreaded automations.  Threaded automations allow multiple browsers to work on jobs at the same time, so your automations can get work done quicker!  [SiteAutomations](https://github.com/Wykleph/Slack/tree/master/SiteAutomations/Examples) are Controllers that control how to interact with each web site.
The SiteAutomations do most of the heavy lifting, so check out the examples._

## [.env](https://github.com/Wykleph/Slack/blob/master/.env) File

The [`.env`](https://github.com/Wykleph/Slack/blob/master/.env) file allows you to define how you want `Selenium` and `peewee` work.  It's essentially a `.ini` file that
holds options for your application.  _Note: Load your `WebDriver` instance using the environment helper functions.  Example in
[`Example.py`](https://github.com/Wykleph/Slack/blob/master/Example.py)_

The default [`.env`](https://github.com/Wykleph/Slack/blob/master/.env) file looks like this:
```python
# Browsers: chrome, firefox, safari, phantomjs, opera
BROWSER=chrome

# Database settings
DB_TYPE=sql
DB=default.db
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=None
DB_PASSWORD=None

# Admin Settings
ADMIN_EMAIL=None

GMAIL_USERNAME=none
GMAIL_PASSWORD=none
GMAIL_HOST=smtp.gmail.com
GMAIL_PORT=587
```
You can tell `Selenium` which browser to use, and you can tell `peewee` all the information about how to connect to your
database.

You can manually set any key/value you do not want to show up in version control inside the [`.env`](https://github.com/Wykleph/Slack/blob/master/.env) file, then use the
`env` helper function located in [`Config.Environment`](https://github.com/Wykleph/Slack/blob/master/Config/Environment.py) to retrieve the values later.

## Creating Models

Models are defined based on `peewee` models, so [check out how to use them](http://docs.peewee-orm.com/en/latest/peewee/models.html)..

Once you have defined your models in [`Project/Models.py`](https://github.com/Wykleph/Slack/blob/master/Project/Models.py), they are accessed using the `Models.ModelName` syntax.

#### Running Migrations on Models

A migration is basically just a way of saying, "create the tables in the database based on our defined models", at least
for now.  Database seeding will be implemented in the near future, however you can run basic migrations to recreate your
database tables based on the models you defined in [`Project/Models.py`](https://github.com/Wykleph/Slack/blob/master/Project/Models.py).  The [`Project/Migrations.py`](https://github.com/Wykleph/Slack/blob/master/Migrations.py) file will use reflection to load
the model attributes and create the tables for you.

Just run the `Migrations.py` file to run your migrations.

## Filtering `WebElement` Instances

Using the [`WebElementFilter`](https://github.com/Wykleph/Slack/blob/master/Helpers/Validation.py) class allows selenium `WebElement` instances to be filtered using wildcard and or regex expressions
on attributes of a web element.  This is helpful when you have elements that have variable attributes like `<td data-tag='x_23'>`, or
`<td data-tag='x_24'>`.  Elements can also be filtered the same way by their inner text.

```python
from Helpers.Validation import WebElementFilter

elements = driver.find_elements_by_xpath('//td')
ele_filt = WebElementFilter()

# Use `filtered_elements = [e for e in elements if ele_filt.inner_text().wildcard_match(e, 'x_*')]`
# to filter based on the inner text of an element.
filtered_elements = [e for e in elements if ele_filt.attribute('data-tag').wildcard_match(e, 'x_*')]
print filtered_elements
```

These could easily be written using the `re` package, but I added it for simplicity, and so the logic
doesn't have to be re-written since it's pretty common to do either type of matches on an elements
attributes.
