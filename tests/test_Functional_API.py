import os

from unittest import TestCase, skipIf
from pyzabbix import ZabbixAPI, ZabbixAPIException


@skipIf('TRAVIS' not in os.environ.keys(), "Travis CI test")
class FunctionalAPI(TestCase):
    def test_LoginToServer(self):
        try:
            ZabbixAPI(url='http://127.0.0.1',
                      user='Admin',
                      password='zabbix')
        except ZabbixAPIException:
            self.fail('Can\'t login to Zabbix')

    def test_LoginToServerSSL(self):
        try:
            ZabbixAPI(url='https://127.0.0.1',
                      user='Admin',
                      password='zabbix')
        except ZabbixAPIException:
            self.fail('Can\'t login to Zabbix')

    def test_get_api_version(self):
        zapi = ZabbixAPI(url='http://127.0.0.1',
                         user='Admin',
                         password='zabbix')
        if os.environ['ZABBIX_VERSION'] == '3':
            self.assertEqual(zapi.api_version(), '3.0.1')
        elif os.environ['ZABBIX_VERSION'] == '2':
            self.assertEqual(zapi.api_version(), '2.4.7')
        else:
            self.fail('api_version() not tested!')
