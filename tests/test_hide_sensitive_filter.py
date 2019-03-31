import unittest
from pyzabbix.logger import HideSensitiveService


class TestHideSensitiveFilter(unittest.TestCase):

    def test_hide_filter_multi(self):

        test_message = '"password": "hide_this", ' \
                       '"result": "0424bd59b807674191e7d77572075f33", ' \
                       '"result": "do_not_hide_this", ' \
                       '"auth": "0424bd59b807674191e7d77572075f33"'
        expected = ('"password": "{}", '
                    '"result": "{}", '
                    '"result": "do_not_hide_this", '
                    '"auth": "{}"').format(
                        HideSensitiveService.HIDEMASK,
                        HideSensitiveService.HIDEMASK,
                        HideSensitiveService.HIDEMASK)

        self.assertEqual(HideSensitiveService.hide_sensitive(test_message),
                         expected)

    def test_hide_filter_do_not_change_url(self):

        # Filter should not hide 'zabbix' in URL:
        # https://localhost/zabbix/api_jsonrpc.php
        test = 'urllib2.Request(https://localhost/zabbix/api_jsonrpc.php,' \
            '{ ... "params": {"user": "Admin", "password": "zabbix"}, '\
            '"id": "1"}))'
        expected = 'urllib2.Request(https://localhost/zabbix/api_jsonrpc.php,'\
            '{ ... "params": {"user": "Admin", "password": "' + \
            HideSensitiveService.HIDEMASK + '"}, "id": "1"}))'

        self.assertEqual(HideSensitiveService.hide_sensitive(test),
                         expected)
