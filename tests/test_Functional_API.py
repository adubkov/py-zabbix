import os

from unittest import TestCase, skipIf
from pyzabbix import ZabbixAPI, ZabbixAPIException


@skipIf('TRAVIS' not in os.environ.keys(), "Travis CI test")
class FunctionalAPI(TestCase):
    def test_LoginToServer(self):
        try:
            zapi = ZabbixAPI(url='http://127.0.0.1',
                             user='Admin',
                             password='zabbix')
        except ZabbixAPIException:
            self.fail('Can\'t login to Zabbix')

    def test_get_api_version(self):
        zapi = ZabbixAPI(url='http://127.0.0.1',
                         user='Admin',
                         password='zabbix')
        self.assertEqual(zapi.api_version(), '3.0.1')
