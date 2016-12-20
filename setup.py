#!/usr/bin/env python

from distutils.core import setup

setup(
        name='Selenext',
        version='0.1dev',
        description='Selenium convenience library.',
        author='Wykleph',
        author_email='someone@somewhere.com',
        url='https://github.com/Wykleph/selenext',
        packages=['selenext'],
        install_requires=[  'peewee', 
                            'selenium', 
                            'requests' , 
                            'beautifulsoup4', 
                            'lxml'
                          ],
        license='NEED LICENSE',
    )