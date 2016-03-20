from unittest import TestCase, skipIf
from zabbix.api import ZabbixAPI, ZabbixAPIException

import os


@skipIf('TRAVIS' not in os.environ.keys(), "Travis CI test")
class FunctionalAPI(TestCase):
    def test_LoginToServer(self):
        try:
            zapi = ZabbixAPI(url='http://127.0.0.1',
                             user='Admin',
                             password='zabbix')
        except ZabbixAPIException:
            self.fail('Can\'t login to Zabbix')

