#!/usr/bin/env python

from setuptools import setup

setup(
        name='selenext',
        version='0.1dev',
        description='Selenium convenience library.',
        author='Wykleph',
        author_email='someone@somewhere.com',
        url='https://github.com/Wykleph/selenext',
        packages=[  'selenext',
                    'selenext.Helpers',
                    'selenext.Helpers.Requests',
                    'selenext.Project',
                    'selenext.Project.Jobs',
                    'selenext.SiteAutomations',
                    'selenext.SiteAutomations.Examples',],
        install_requires=[  'peewee', 
                            'selenium', 
                            'requests' , 
                            'beautifulsoup4', 
                            'lxml'
                          ],
        license='Apache License Version 2.0',
    )