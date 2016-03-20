.. _quickstart_guide:

===========================
Quickstart guide
===========================

Install
=======

You can install Zabbix modules for Python with pip:

.. code-block:: bash

    pip install py-zabbix

Usage examples
==============

Example zabbix.api
------------------

::

    result = zapi.host.getobjects(status=1)


Example zabbix.sender
---------------------

::

    metrics= [ZabbixMetric('localhost', 'cpu[usage]', '15.4')]
    ZabbixSender(use_config=True).send(metrics)
