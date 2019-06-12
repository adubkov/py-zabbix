|Build Status| |Coverage| |PyPi status| |PyPi version|

Zabbix module for Python
========================

Install
-------

You can install Zabbix modules for Python with pip:

::

    pip install py-zabbix

Official documentation for `py-zabbix <https://py-zabbix.readthedocs.org/en/latest/>`__
--------------------------------------------------------------------------------------

Examples
--------

ZabbixAPI
~~~~~~~~~

.. code:: python

    from pyzabbix.api import ZabbixAPI

    # Create ZabbixAPI class instance
    zapi = ZabbixAPI(url='https://localhost/zabbix/', user='Admin', password='zabbix')

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

    # Logout from Zabbix
    zapi.user.logout()

Or use 'with' statement to logout automatically:

.. code:: python

    from pyzabbix.api import ZabbixAPI

    # Create ZabbixAPI class instance
    with ZabbixAPI(url='https://localhost/zabbix/', user='Admin', password='zabbix') as zapi:

        # Get all monitored hosts
        result1 = zapi.host.get(monitored_hosts=1, output='extend')

Enable logging:

.. code:: python

    import sys
    import logging
    from pyzabbix.api import ZabbixAPI

    # Create ZabbixAPI class instance
    logger = logging.getLogger("pyzabbix")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    zapi = ZabbixAPI(url='http://localhost', user='Admin', password='zabbix')

Note that passwords and auth tokens are hidden when raw messages are logged or raised in exceptions ( but not hidden if print() is used):

.. code:: python

    ZabbixAPI.login(Admin,********)
    Call user.login method
    urllib2.Request(http://localhost/api_jsonrpc.php, {"jsonrpc": "2.0", "method": "user.login", "params": {"user": "Admin", "password": "********"}, "id": "1"})
    Response Body: {
        "jsonrpc": "2.0",
        "result": "********",
        "id": "1"
    }


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
.. |PyPi status| image:: https://img.shields.io/pypi/status/py-zabbix.svg
   :target: https://pypi.python.org/pypi/py-zabbix/
.. |PyPi version| image:: https://img.shields.io/pypi/v/py-zabbix.svg
   :target: https://pypi.python.org/pypi/py-zabbix/
