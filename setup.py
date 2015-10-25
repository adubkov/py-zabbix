#!/usr/bin/env python
from setuptools import setup

import os

base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, 'zabbix', 'version.py')) as f:
    exec(f.read(), about)

setup(name='py-zabbix',
      version=about['__version__'],
      description='Python modules for work with zabbix.',
      url='https://github.com/blacked/py-zabbix',
      author='Alexey Dubkov',
      author_email='alexey.dubkov@gmail.com',
      packages=['zabbix']
     )
