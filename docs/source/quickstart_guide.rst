.. _quickstart_guide:

################
Quickstart guide
################

=======
Install
=======

You can install Zabbix modules for Python with pip:

.. code-block:: bash

    pip install py-zabbix

========
Examples
========

---------
ZabbixAPI
---------

You can make zabbix api call with two ways.

1. By With dynamicaly mapping :class:`pyzabbix.api.ZabbixAPI` methods on zabbix api:

::

    result = zapi.host.get(status=1)

2. By passing zabbix api function and arguments as parameters:

::

    result = zapi.do_request('host.get', {'status':1})

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Get list of not monitored hosts from zabbix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pyzabbix import ZabbixAPI

    # Create ZabbixAPI class instance
    zapi = ZabbixAPI(url='https://localhost/zabbix/', user='admin', password='zabbix')

    # Get all disabled hosts
    result1 = zapi.host.get(status=1)
    hostnames = [host['host'] for host in result1]

    # Other way to get all disabled hosts
    result2 = zapi.do_request('host.get', {'status':1})
    hostnames2 = [host['host'] for host in result2['result']]


------------
ZabbixSender
------------
~~~~~~~~~~~~~~~~~~~~~
Send metric to zabbix
~~~~~~~~~~~~~~~~~~~~~

::

    metrics= [ZabbixMetric('localhost', 'cpu[usage]', '15.4')]
    ZabbixSender(use_config=True).send(metrics)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Usage with zabbix_agentd.conf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If your box already have zabbix_agent installed. Py-zabbix can use zabbix server
from zabbix_agentd.conf file.

::

    from pyzabbix import ZabbixMetric, ZabbixSender

    packet = [
      ZabbixMetric('centos', 'test[cpu_usage]', 2),
      ZabbixMetric('centos', 'test[system_status]', "OK"),
      ZabbixMetric('centos', 'test[disk_io]', '0.1'),
      ZabbixMetric('centos', 'test[cpu_usage]', 20, 1411598020),
      ZabbixMetric('centos', 'test[cpu_usage]', 30, 1411598120),
      ZabbixMetric('centos', 'test[cpu_usage]', 40, 1411598240),
    ]

    sender = ZabbixSender(use_config=True)
    sender.send(packet)
