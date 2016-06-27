import os

from unittest import TestCase, skipIf
from time import time as now

from pyzabbix import ZabbixMetric, ZabbixSender, ZabbixResponse


@skipIf('TRAVIS' not in os.environ.keys(), "Travis CI test")
class FunctionalSender(TestCase):
    def test_sendMetricsToServer(self):
        cur_date_unix = int(now())
        m = [
            ZabbixMetric('host2', 'key3', 'IDDQD'),
            ZabbixMetric('host1', 'key1', 33.1, cur_date_unix)
        ]

        z = ZabbixSender('127.0.0.1', 10051, chunk_size=1).send(m)

        self.assertIsInstance(z, ZabbixResponse)
        self.assertEqual(z.total, 2)
        self.assertEqual(z.processed, 2)
        self.assertEqual(z.failed, 0)
        self.assertEqual(z.chunk, 2)
