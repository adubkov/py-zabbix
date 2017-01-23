import json

from unittest import TestCase
from pyzabbix import ZabbixAPI, ssl_context_compat
try:
    from mock import patch
except ImportError:
    from unittest.mock import patch
from sys import version_info

# For Python 2 and 3 compatibility
if version_info[0] == 2:
    urlopen = 'urllib2.urlopen'
    res_type = str
elif version_info[0] >= 3:
    res_type = bytes
    urlopen = 'urllib.request.urlopen'


class MockResponse(object):

    def __init__(self, ret, code=200, msg='OK'):
        self.ret = ret
        self.code = code
        self.msg = msg
        self.headers = {'content-type': 'text/plain; charset=utf-8'}

    def read(self):
        return res_type(self.ret.encode('utf-8'))

    def getcode(self):
        return self.code


class TestZabbixAPI(TestCase):

    def setUp(self):
        "Mock urllib2.urlopen"
        self.patcher = patch(urlopen)
        self.urlopen_mock = self.patcher.start()

    def test_decorator_ssl_context_compat(self):
        @ssl_context_compat
        def test_decorator(*args, **kwargs):
            def response(*args, **kwargs):
                return args, kwargs
            return response(*args, **kwargs)

        arg, context = test_decorator(True)
        self.assertIs(arg[0], True)
        self.assertIn('context', context, msg='SSL context is missing.')
        self.assertIsNotNone(context.get('context'),
                             msg='SSL context is None.')

    def test_api_version(self):
        ret = {'result': '2.2.5'}
        self.urlopen_mock.return_value = MockResponse(json.dumps(ret))
        res = ZabbixAPI().api_version()
        self.assertEqual(res, '2.2.5')

    def test_login(self):
        req = {'user': 'admin', 'password': 'zabbix'}
        ret = {
            'jsonrpc': '2.0',
            'result': '0424bd59b807674191e7d77572075f33',
            'id': 1
        }
        self.urlopen_mock.return_value = MockResponse(json.dumps(ret))
        res = ZabbixAPI().user.login(**req)
        self.assertEqual(res, '0424bd59b807674191e7d77572075f33')

    def test_do_request(self):
        req = 'apiinfo.version'
        ret = {
            'jsonrpc': '2.0',
            'result': '2.2.5',
            'id': 1
        }
        self.urlopen_mock.return_value = MockResponse(json.dumps(ret))
        res = ZabbixAPI().do_request(req)
        self.assertEqual(res, ret)

    def test_get_id_item(self):
        ret = {
            'jsonrpc': '2.0',
            'result':
            [{
                'itemid': '23298',
                'hostid': '10084',
                'name': 'Test Item',
                'key_': 'system.cpu.switches',
                'description': '',
            }],
            'id': 1,
        }
        self.urlopen_mock.return_value = MockResponse(json.dumps(ret))
        res = ZabbixAPI().get_id('item', item='Test Item')
        self.assertEqual(res, 23298)

    def tearDown(self):
        self.patcher.stop()
