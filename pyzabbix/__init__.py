import pyzabbix.version

from .api import ZabbixAPI, ZabbixAPIException
from .sender import ZabbixMetric, ZabbixSender

__version__ = pyzabbix.version.__version__
