from unittest import TestCase, skipIf
from zabbix.sender import ZabbixMetric, ZabbixSender

from datetime import datetime
import os


class FunctionalSender(TestCase):
    @skipIf('TRAVIS' not in os.environ.keys(),
            "Travis CI test")
    def test_sendMetricsToServer(self):
        cur_date_unix = int(datetime.now().timestamp())
        m = [
            ZabbixMetric('host2', 'key3', 'IDDQD'),
            ZabbixMetric('host1', 'key1', 33.1, cur_date_unix)
        ]

        z = ZabbixSender('127.0.0.1', 10051).send(m)
        self.assertEqual(z, True)
