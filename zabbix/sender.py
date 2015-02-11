import base64
import ConfigParser
import json
import logging
import socket
import StringIO
import struct
import sys
import time
import urllib2

logger = logging.getLogger(__name__)

class ZabbixMetric(object):
  """
  Create structure contains metric for zabbix server.

  Attributes:
    host (str): Hostname as it displays in Zabbix.
    key (str):  Key by which you will identify this metric.
    value (*):  Key value.
    clock (int): A timestamp in seconds. If None, then it will current time

  Example:
    >> ZabbixMetric('localhost', 'cpu[usage]', 20)
  """

  def __init__(self, host, key, value, clock = None):
    self.host = str(host)
    self.key = str(key)
    self.value = str(value)
    self.clock = clock if clock else str(int(time.time()))

  def __repr__(self):
    """
    Represent detailed ZabbixMetric view.
    """

    result = json.dumps(self.__dict__)
    logger.debug('{0}: {1}'.format(self.__class__.__name__, result))

    return result


class ZabbixSender(object):
  """
  Send ZabbixMetrics to Zabbix server, like zabbix_sender util.
  Implement zabbix trapper protocol.

  Attributes:
    zabbix_server (str):  IP address of Zabbix server. Default: 127.0.0.1

    zabbix_port (int):    Port of Zabbix server. Default: 10051

    use_config (str):     Specify config file from which zabbix_server
                          and zabbix_port will be loaded.

                          If True then use default config:
                            /etc/zabbix/zabbix_agentd.conf
  """

  def __init__(self, zabbix_server = '127.0.0.1', zabbix_port = 10051, use_config = None):

    self.cn = self.__class__.__name__

    if use_config:
      self.zabbix_uri = self.__load_from_config(use_config)
    else:
      self.zabbix_uri = [ (zabbix_server, zabbix_port) ]

    logger.debug('{0}({1})'.format(self.cn, self.zabbix_uri))

  def __load_from_config(self, config_file):
    """
    Load zabbix server ip address and port from zabbix agent file

    If Server or Port variable won't be found if the file, they will be
    seted up from defaults: 127.0.0.1:10051
    """

    if config_file and isinstance(config_file, bool):
      config_file = '/etc/zabbix/zabbix_agentd.conf'

    result = None

    try:
      """This is workaround for config wile without sections"""
      with open(config_file, 'r') as f:
        config_file_data = "[root]\n" + f.read()
    except:
      result = False
      exit()

    config_file_fp = StringIO.StringIO(config_file_data)
    config = ConfigParser.RawConfigParser({'Server':'127.0.0.1', 'Port':10051})
    config.readfp(config_file_fp)
    zabbix_server = config.get('root','Server')
    zabbix_port = config.get('root','Port')
    zabbix_server_list = [ server.strip() for server in zabbix_server.split(',')]

    result = [ (server, zabbix_port) for server in zabbix_server_list ]

    return result

  def __receive(self, socket, count):
    """
    Reads socket to receive data from zabbix server.

    Attributes:
      socket (socket):  Socket object from which data should be read
      count (int):  Amount of data that should be read from socket, in bytes.
    """

    buf = ''

    while len(buf) < count:
      chunk = socket.recv(count - len(buf))
      if not chunk:
        break
      buf += chunk

    return buf

  def __create_messages(self, metrics_array):
    """
    Create a list of zabbix messages, from a list of ZabbixMetrics.

    Attributes:
      metrics_array (list of ZabbixMetrics): List of ZabbixMetrics

    Returns:
      list of str: List of zabbix messages
    """

    metrics = []

    # Fill the array of messages
    for m in metrics_array:
      metrics.append(str(m))

    logger.debug('{0}.__create_messages: {1}'.format(self.cn, metrics))

    return metrics

  def __create_request(self, messages):
    """
    Create a formated request to zabbix from a list of messages.

    Attributes:
      messages (list of str): List zabbix messages

    Returns:
      str: Formated request to zabbix
    """

    request = '{{"request":"sender data","data":[{0}]}}'.format(','.join(messages))
    logger.debug('{0}.__create_request: {1}'.format(self.cn, request))

    return request

  def __create_packet(self, request):
    """
    Create a formated packet from a request.

    Attributes:
      request (str): Request string to zabbix

    Returns:
      str: Packet string to zabbix
    """

    data_len = struct.pack('<Q', len(request))
    packet = 'ZBXD\x01'+ data_len + request
    logger.debug('{0}.__create_packet (str): {1}'.format(self.cn, packet))
    logger.debug('{0}.__create_packet (hex): {1}'.format(self.cn,
      ':'.join(x.encode('hex') for x in packet)))

    return packet

  def __get_response(self, connection):
    """
    Get response from zabbix server, reads from self.socket.

    Returns:
      str: JSON response from zabbix server
    """

    result = None
    response_header = self.__receive(connection, 13)
    logger.debug('{0}.__get_response.response_header: {1}'.format(self.cn, response_header))

    if not response_header.startswith('ZBXD\x01') or len(response_header) != 13:
      logger.debug('{0}.__get_response: Wrong zabbix response'.format(self.cn))
      result = False
    else:
      response_len = struct.unpack('<Q', response_header[5:])[0]

      try:
        response_body = connection.recv(response_len)
      finally:
        connection.close()

      result = json.loads(response_body)
      logger.debug('{0}.__get_response: {1}'.format(self.cn, result))

    return result

  def send(self, metrics):
    """
    Send the metrics to zabbix server.

    Attributes:
      metrics (list of ZabbixMetrics): List of metrics that will be send to Zabbix

    Returns:
      bool: True if sent successful, False if was an error.
    """

    result = None

    messages = self.__create_messages(metrics)
    request = self.__create_request(messages)
    packet = self.__create_packet(request)

    for host_addr in self.zabbix_uri:
      logger.debug('{0}.send({1}): connecting'.format(self.cn, host_addr))

      # create socket object
      connection  = socket.socket()

      # server and port must be tuple
      connection.connect(host_addr)

      try:
        connection.sendall(packet)
      except Exception, e:
        logger.debug("{0}.send: Error while sending the data to zabbix\nERROR:{1}".format(self.cn, e))
        connection.close()
        exit()

      # socket will be closed in self._get_response()
      response = self.__get_response(connection)
      logger.debug('{0}.send({1}): {2}'.format(self.cn, host_addr, response))

      if response.get('response') == 'success':
        result = True
      else:
        logger.debug('{0}.send: Got error from zabbix => {1}'.format(self.cn, response))
        raise Exception('Zabbix Server ({0}) reject packet.'.format(host_addr))

    return result
