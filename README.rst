|Build Status| |Coverage| |PyPi downloads| |PyPi version|

Zabbix module for Python
========================

Install
-------

You can install Zabbix modules for Python with pip:

::

    pip install py-zabbix

Official documentaion for `py-zabbix <https://py-zabbix.readthedocs.org/en/latest/>`__
--------------------------------------------------------------------------------------

Examples
--------

ZabbixAPI
~~~~~~~~~

.. code:: python

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

ZabbixSender
~~~~~~~~~~~~

.. code:: python

    from pyzabbix import ZabbixMetric, ZabbixSender

    # Send metrics to zabbix trapper
    packet = [
      ZabbixMetric('hostname1', 'test[cpu_usage]', 2),
      ZabbixMetric('hostname1', 'test[system_status]', "OK"),
      ZabbixMetric('hostname1', 'test[disk_io]', '0.1'),
      ZabbixMetric('hostname1', 'test[cpu_usage]', 20, 1411598020),
    ]

    result = ZabbixSender(use_config=True).send(packet)

.. |Build Status| image:: https://travis-ci.org/adubkov/py-zabbix.svg?branch=master
   :target: https://travis-ci.org/adubkov/py-zabbix
.. |Coverage| image:: https://coveralls.io/repos/github/adubkov/py-zabbix/badge.svg?branch=master
   :target: https://coveralls.io/github/adubkov/py-zabbix?branch=master
.. |PyPi downloads| image:: https://img.shields.io/pypi/dm/py-zabbix.svg
   :target: https://pypi.python.org/pypi/py-zabbix/
.. |PyPi version| image:: https://img.shields.io/pypi/v/py-zabbix.svg
   :target: https://pypi.python.org/pypi/py-zabbix/
