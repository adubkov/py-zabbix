[![Build Status](https://travis-ci.org/blacked/py-zabbix.svg?branch=master)](https://travis-ci.org/blacked/py-zabbix)
[![PyPi downloads](https://img.shields.io/pypi/dm/py-zabbix.svg)](https://pypi.python.org/pypi/py-zabbix/)
[![PyPi version](https://img.shields.io/pypi/v/py-zabbix.svg)](https://pypi.python.org/pypi/py-zabbix/)
[![License](https://img.shields.io/github/license/blacked/py-zabbix.svg)](https://github.com/blacked/py-zabbix/blob/master/LICENSE)

# Zabbix module for Python

## Install

You can install Zabbix modules for Python with pip:
```
pip install py-zabbix
```

## Official documentaion for [py-zabbix](https://py-zabbix.readthedocs.org/en/latest/)

## Examples

### ZabbixAPI

```python
from zabbix.api import ZabbixAPI

# Create ZabbixAPI class instance
zapi = ZabbixAPI(url='https://localhost/zabbix/', user='admin', password='zabbix')

# Get all monitored hosts
result1 = zapi.host.get(monitored_hosts=1, output='extend')

# Get all disabled hosts
result2 = zapi.do_request('host.get',
						  {
						  	  'filter': {'status': 1},
	 					  	  'output': 'extend'
						  })

# Filter results
hostnames1 = [host['host'] for host in result1]
hostnames2 = [host['host'] for host in result2['result']]
```

### ZabbixSender

```python
from pyzabbix import ZabbixMetric, ZabbixSender

# Send metrics to zabbix trapper
packet = [
  ZabbixMetric('hostname1', 'test[cpu_usage]', 2),
  ZabbixMetric('hostname1', 'test[system_status]', "OK"),
  ZabbixMetric('hostname1', 'test[disk_io]', '0.1'),
  ZabbixMetric('hostname1', 'test[cpu_usage]', 20, 1411598020),
]

result = ZabbixSender(use_config=True).send(packet)
```
