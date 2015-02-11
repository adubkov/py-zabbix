import logging
from zabbix.sender import ZabbixMetric, ZabbixSender

logging.basicConfig(level = logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

m = [
  ZabbixMetric('centos', 'test[cpu_usage]', 2),
  ZabbixMetric('centos', 'test[system_status]', "OK"),
  ZabbixMetric('centos', 'test[disk_io]', '0.1'),
  ZabbixMetric('centos', 'test[http_req_per_sec]', 15),
  ZabbixMetric('centos', 'test[app_status]', 200),
  ZabbixMetric('centos', 'test[cpu_usage]', 20, 1411598020),
  ZabbixMetric('centos', 'test[cpu_usage]', 30, 1411598120),
  ZabbixMetric('centos', 'test[cpu_usage]', 40, 1411598220),
  ZabbixMetric('centos', 'test[cpu_usage]', 80, 1411598320),
  ZabbixMetric('centos', 'test[cpu_usage]', 30, 1411598420),
]

z = ZabbixSender(use_config=True).send(m)
