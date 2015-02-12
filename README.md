# Zabbix module for Python
That set of modules allow to work with Zabbix in Python.

Curretnly it contain:
* Module for work with Zabbix API
* Module for send metrics to Zabbix.

Those modules not require addition modules, they use standard Python modules.

# Install

You can install Zabbix modules for Python with pip:
```
pip install py-zabbix
```

## API

This module provide classes to work with Zabbix API.

### ZabbixAPI
Implement interface to Zabbix API.

#### Make request to Zabbix API
You can make zabbix api call with two ways:
```python
result = zapi.host.getobjects(status=1)
```
or
```python
result = zapi.do_request('host.getobjects', {'status':1})
```

#### Get Zabbix API version
```python
api_version()
```

#### Get object ID
Return id or list with id of zabbix objects.

```
get_id(item_type, item=None, with_id=False, hostid=None, **args)

    item_type   (str): Type of zabbix object
    item        (str): Name of zabbix object
                      If None - will return list of all object in the scope
    with_id    (bool): Return values will be in zabbix format
                      Examlpe: {'itemid: 128}
    hostid      (int): Specify id of host for special cases
    templateid  (int): Specify scope to specific template
    app_name    (str): Specify scope to specific template
```

#### Example:
```python
from zabbix.api import ZabbixAPI

# Create ZabbixAPI class instance
zapi = ZabbixAPI(url='https://localhost/zabbix/', user='admin', password='zabbix')

# Get all disabled hosts
result1 = zapi.host.getobjects(status=1)

# Other way to get all disabled hosts
result2 = zapi.do_request('host.getobjects', {'status':1})

hostnames1 = [host['host'] for host in result1]
hostnames2 = [host['host'] for host in result2['result']]
```

### ZabbixAPIObjectClass
That class dinamicaly map method to Zabbix API call.


## Sender

This module provide classes to send metrics to Zabbix.

### ZabbixMetric Class

ZabbixMetric class create metric-message to zabbix. Each message contains:
* Hostname
* Key
* Value
* Timestamp (current time using if not specified)

#### Example:
```python
message = ZabbixMetric('localhost', 'cpu[usage]', '15.4')
```

### ZabbixSender Class

ZabbixSender class allow send list of ZabbixMetric objects to Zabbix.

You can specify endpoint of zabbix to which you want send the message:
```python
ZabbixSender('zabbix.local', 10051).send( ... )
```

or use zabbix setting from agent config file for that:
```python
ZabbixSender(use_config = True).send( ... )
```

Example:
```python
from zabbix.sender import ZabbixMetric, ZabbixSender

packet = [
  ZabbixMetric('centos', 'test[cpu_usage]', 2),
  ZabbixMetric('centos', 'test[system_status]', "OK"),
  ZabbixMetric('centos', 'test[disk_io]', '0.1'),
  ZabbixMetric('centos', 'test[cpu_usage]', 20, 1411598020),
  ZabbixMetric('centos', 'test[cpu_usage]', 30, 1411598120),
  ZabbixMetric('centos', 'test[cpu_usage]', 40, 1411598240),
]

result = ZabbixSender(use_config=True).send(packet)
```
