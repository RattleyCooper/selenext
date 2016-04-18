# Slack
Slack is a micro-framework for simple web scraping using selenium.  A lot about how the framework operates was inspired by the
Laravel framework(PHP), which used for created web-applications.

## About

One of the benefits of using `Slack` is the ability to run middleware on your `peewee` models using `Jambi`.  `Jambi` uses reflection
to find middleware and runs the appropriate middleware methods automatically.  This takes care of data manipulation on the database
side of things pretty well.  The idea of `SiteAutomations` was also implimented to give a command-like structure to your automation
flow.  Writing all of your automations inside of a `SiteAutomation` keeps things modular and neatly organized.  There are also
helper methods for filtering web elements returned by `Selenium`'s `find_elements` method(more on that later).

You end up with a pretty clean area for piecing together your automations:

```python
import Models
from Config.Environment import env, env_driver
from Helpers.Contexts import quitting
from Helpers.Database import Jambi

# `SiteAutomations` holds the code that drives selenium's `WebDriver` instance.
# Create a file and class in the `SiteAutomations` folder for each site you are
# automating.
from SiteAutomations import GoogleExample

# More on `Jambi` later.
jambi = Jambi()

# Use a different browser by modifying your `.env` file.
with quitting(env_driver(env("BROWSER"))()) as driver:
    google_search = GoogleExample.Search(driver, jambi)

    # Do Search
    google_search.perform_search('google wiki')
    sleep(1)

    # Do scrape
    results = google_search.scrape_wikipedia_href_results()
    print results
    sleep(5)
```

_Check out the __`Example.py`__ file for more detailed documentation on the workflow_

## Dependencies

* [peewee](http://docs.peewee-orm.com/en/latest/)
`pip install peewee`
* [selenium python bindings](http://selenium-python.readthedocs.org/)

Once you have the dependencies, you can download this repository and start using it as is, however you may want to read over the
documentation below.

__There is an `Example.py` file that shows exactly what an application looks like when utilizing the `Slack`
framework.  `Example.py` can be used as a template.__

## .env File

The `.env` file allows you to define how you want `Selenium` and `peewee` work.  It's essentially a `.ini` file that
holds options for your application.

The default `.env` file looks like this:
```python
# Note the lack of quotes.  Don't use quotes when setting these options.
# Browsers: chrome, firefox, safari, phantomjs, opera
BROWSER=chrome

# Database settings
DB_TYPE=sql
DB=default.db
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=None
DB_PASSWORD=None
```
You can tell `Selenium` which browser to use, and you can tell `peewee` all the information about how to connect to your
database.

You can manually set any key/value you do not want to show up in version control inside the `.env` file, then use the
`env` helper function located in `Config.Environment` to retrieve the values later.

## Creating Models and Middleware using genesis.py

### Models
Models are defined based on `peewee` models, so [check out how to use them](http://docs.peewee-orm.com/en/latest/peewee/models.html)..

Create models using the following syntax in the command line:

`python genesis.py make:model ModelName`.

If you are on windows, it might look something like:

`c:/python27/python.exe c:/path/to/genesis.py make:model ModelName`.

The models are appended to the `Models.py` file, and any changes can be made in the `Models.py`
file. __This will probably change to operate similar to the middleware classes in the future.__

Once you have defined your models, they are accessed using the `Models.ModelName` syntax.

#### Running Migrations on Models

A migration is basically just a way of saying, "create the tables in the database based on our defined models", at least
for now.  Database seeding will be implemented in the near future, however you can run basic migrations to recreate your
database tables based on the models you defined in `Models.py`.  The `Migrations.py` file will use reflection to load
the model attributes and create the tables for you.

To run migrations, use the following syntax:

`python genesis.py run:migrations`

You can also run the `Migrations.py` file by itself.  Either way will run migrations for all of your defined models.

### Middleware & Jambi

A piece of middleware is defined based on the name of the model the middleware should operate on.  It's only
purpose it to modify data before it is entered into the database, or modify data after it is pulled from the
database.

Middleware for the models is generated when you create a model with `genesis.py` and the files can be found in the
`middleware` folder.  Methods are automatically generated for each attribute that is defined on a model and if you
use the database helper, `Jambi`, to run your model methods, the middleware will run automatically(Example later).

Middleware for a generated model looks like this(without the example value modifications/comments I added):

```python
class UserMiddleware(Middleware):
  # Whenever User data is added to the database, the attribute's `set_attribute` method will be called.
  def set_created_at(self, value):
      if value == '':
        value = 'False'
      return value

  # Whenever User data is pulled, the attribute's `get_attribute` method will be called on the result.
  def get_created_at(self, value):
      if value == 'False':
        value = False
      return value
```

This is because a generated model only has a `created_at` attribute. If we ran `genesis.py make:model User --no-middleware`,
we could add attributes to our model, then run `genesis.py make:middleware User` to create the base middleware for our `User`
model.  Also, as you can see, the syntax for any middleware method is either `set_` + the attribute name, if you want data
to be modified going in, and `get_` + attribute name if you want data to be modified coming out of the database.

The way we run middleware is by passing the model's method along with the data to one of `Jambi`'s
methods.  Example:

```python
# pull in appropriate modules / packages.
import Models
from Helpers.Database import Jambi

jambi = Jambi()
credentials = {
  'username': 'SomeGuyNamedBobby',
  'email': 'bobby@domain.com',
  'password': 'password_for_site'
}
user = jambi.model_func(Models.User.get_or_create, **credentials)
print user
```

_Note:  It's important to test the data you get back from `Jambi` since it will return a `peewee` model instance,
a dictionary or a `boolean`._

## Filtering `WebElement` Instances

Using the `WebElementFilter` class allows selenium `WebElement` instances to be filtered using wildcard and or regex expressions
on attributes of a web element.  This is helpful when you have elements that have variable attributes like `<td data-tag='x_23'>`, or
`<td data-tag='x_24'>`.  Elements can also be filtered the same way by their inner text.

```python
elements = driver.find_elements_by_xpath('//td)
ele_filt = WebElementFilter()

# Use `filtered_elements = [e for e in elements if ele_filt.inner_text().wildcard_match(e, 'x_*')]`
# to filter based on the inner text of an element.
filtered_elements = [e for e in elements if ele_filt.attribute('data-tag').wildcard_match(e, 'x_*')]
print filtered_elements
```

These could easilly be written using the `re` package, but I added it for simplicity, and so the logic
doesn't have to be re-written since it's pretty common to do either type of matches on an elements
attributes.
