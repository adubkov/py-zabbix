#!/usr/bin/env python3
"""Setup of py-zabbix."""

from setuptools import setup
from pyzabbix import __version__

setup(
    name='py-zabbix',
    version=__version__,
    description='Python module to work with zabbix.',
    long_description="It's a fork of https://github.com/adubkov/py-zabbix" +
    "\n\n" +
    open('README.md', 'r').read() +
    '\n\n' +
    open('CHANGELOG.md', 'r').read(),
    url='https://github.com/nixargh/py-zabbix',
    author='nixargh',
    author_email='nixargh@protonmail.com',
    test_suite='tests',
    packages=['pyzabbix'],
    tests_require=['mock'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration'
    ])
