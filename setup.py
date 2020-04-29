#!/usr/bin/env python
from setuptools import setup
from pyzabbix.version import __version__

setup(name='py-zabbix',
      version=__version__,
      description='Python module to work with zabbix.',
      long_description_content_type="text/markdown",
      long_description=open('README.rst', 'r').read(),
      url='https://github.com/blacked/py-zabbix',
      author='Alexey Dubkov',
      author_email='alexey.dubkov@gmail.com',
      test_suite='tests',
      packages=['pyzabbix', 'zabbix'],
      tests_require=['mock'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Monitoring',
          'Topic :: System :: Networking :: Monitoring',
          'Topic :: System :: Systems Administration'
      ]
      )
