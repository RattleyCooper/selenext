selenext is a micro-framework for web automation/scraping using selenium in Python 2 or Python 3.  This is currently still in development, however it's possible to write and run your automations within the framework as it is.

## Install

Just download this as a .zip and then unzip the `selenext` directory into 
your `site-packages` folder. Once there is a stable release, there will 
be a pip install available.  You can also grab the repository and pull
updates from github, just create a symbolic link to the selenext directory
into your python path.

## Dependencies

selenext is pretty modular, so you should only need the dependencies for
the pieces you are using.  For database interaction, install:

* [peewee](http://docs.peewee-orm.com/en/latest/)
`pip install peewee` + installing peewee's dependencies.

You'll need Selenium for doing any browser automation or web scraping. 

* [selenium python bindings](http://selenium-python.readthedocs.org/)
`pip install selenium`

You also need the a Web Driver executable like [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## Optional Dependencies

If you want to use the `requests` module along with `BeautifulSoup/lxml` 
to read the content off a web page using the same API as selenium, you 
can use the `WebReader` class to do so.  It only supports reading 
information off of a page, so methods like `click` are not implemented.
To use the `WebReader`, you will need:

* [requests](http://docs.python-requests.org/en/master/)
`pip install requests`
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
* [lxml](http://lxml.de/)

If you need to spin some text, check out [spintax](https://github.com/AceLewis/spintax) for python!

Once you have the dependencies, you can download this repository and 
start using it, however you may want to read over the documentation 
below.

## Examples

Check out [the documentation](https://github.com/Wykleph/selenext/wiki/Documentation) for the various parts and pieces in the wiki. API documentation will be coming soon.
