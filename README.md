# Zabbix module for Python

## Install
```
git clone https://github.com/nixargh/py-zabbix.git
cd ./py-zabbix
pip3 install -e ./
```

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
