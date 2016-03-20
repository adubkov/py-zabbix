import warnings

from pyzabbix import ZabbixMetric, ZabbixSender

warnings.warn("Module '{name}' was deprecated, use 'pyzabbix' instead."
              "".format(name=__name__), DeprecationWarning)
