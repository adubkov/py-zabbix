#!/usr/bin/env python3
"""Setup of py-zabbix."""

import re
from setuptools import setup


def get_variable_from_file(ffile, variable):
    """Get variable from file."""
    variable_re = "^{} = ['\"]([^'\"]*)['\"]".format(variable)
    with open(ffile, "r") as ffile_obj:
        match = re.search(variable_re, ffile_obj.read(), re.M)
    if match:
        return match.group(1)
    return None


def get_version():
    """Get package version."""
    return get_variable_from_file("pyzabbix/__init__.py", "__version__")

setup(
    name='zabbix',
    version=get_version(),
    description='Python module to work with zabbix.',
    long_description_content_type='text/markdown',
    long_description="**It's a fork of** "
    "<https://github.com/adubkov/py-zabbix>.\n\n" +
    open('README.md', 'r').read() +
    '\n\n' +
    "# CHANGELOG \n" +
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
