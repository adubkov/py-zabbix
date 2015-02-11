import logging
from zabbix.api import ZabbixAPI

logging.basicConfig(level = logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

z = ZabbixAPI(url='https://localhost/zabbix/', user='admin', password='zabbix')

t1 = z.host.getobjects(status=1})
t2 = z.do_request('host.getobjects', {'status':1})

[host['host'] for host in t1]
[host['host'] for host in t2['result']]
