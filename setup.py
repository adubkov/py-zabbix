#!/usr/bin/env python
from setuptools import setup
from pyzabbix import __version__

setup(name='py-zabbix',
      version=__version__,
      description='Python modules to work with zabbix.',
      url='https://github.com/blacked/py-zabbix',
      author='Alexey Dubkov',
      author_email='alexey.dubkov@gmail.com',
      test_suite='tests',
      packages=['pyzabbix','zabbix'],
      tests_require=['mock'],
      )
