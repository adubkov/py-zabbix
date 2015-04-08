import ConfigParser
import json
import logging
import socket
import StringIO
import struct
import time

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

    def __init__(self, host, key, value, clock=None):
        self.host = str(host)
        self.key = str(key)
        self.value = str(value)
        self.clock = clock if clock else str(int(time.time()))

    def __repr__(self):
        """
        Represent detailed ZabbixMetric view.
        """

        result = json.dumps(self.__dict__)
        logger.debug('%s: %s', self.__class__.__name__, result)

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

    def __init__(self, zabbix_server='127.0.0.1', zabbix_port=10051, use_config=None):

        self.cn = self.__class__.__name__

        if use_config:
            self.zabbix_uri = self.__load_from_config(use_config)
        else:
            self.zabbix_uri = [(zabbix_server, zabbix_port)]

        logger.debug('%s(%s)', self.cn, self.zabbix_uri)

    @classmethod
    def __load_from_config(cls, config_file):
        """
        Load zabbix server ip address and port from zabbix agent file

        If Server or Port variable won't be found in the file, they will be
        set up from defaults: 127.0.0.1:10051
        """

        if config_file and isinstance(config_file, bool):
            config_file = '/etc/zabbix/zabbix_agentd.conf'

        try:
            #  This is workaround for config wile without sections
            with open(config_file, 'r') as f:
                config_file_data = "[root]\n" + f.read()
        except:
            exit()

        config_file_fp = StringIO.StringIO(config_file_data)
        config = ConfigParser.RawConfigParser({'Server': '127.0.0.1', 'Port': 10051})
        config.readfp(config_file_fp)
        zabbix_server = config.get('root', 'Server')
        zabbix_port = config.get('root', 'Port')
        zabbix_server_list = [server.strip() for server in zabbix_server.split(',')]

        result = [(server, zabbix_port) for server in zabbix_server_list]

        return result

    @classmethod
    def __receive(cls, sock, count):
        """
        Reads socket to receive data from zabbix server.

        Attributes:
          socket (socket):  Socket object from which data should be read
          count (int):  Amount of data that should be read from socket, in bytes.
        """

        buf = ''

        while len(buf) < count:
            chunk = sock.recv(count - len(buf))
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

        logger.debug('%s.__create_messages: %s', self.cn, metrics)

        return metrics

    def __create_request(self, messages):
        """
        Create a formatted request to zabbix from a list of messages.

        Attributes:
          messages (list of str): List zabbix messages

        Returns:
          str: Formatted request to zabbix
        """

        request = '{"request":"sender data","data":[%s]}' % ','.join(messages)
        logger.debug('%s.__create_request: %s', self.cn, request)

        return request

    def __create_packet(self, request):
        """
        Create a formatted packet from a request.

        Attributes:
          request (str): Request string to zabbix

        Returns:
          str: Packet string to zabbix
        """

        data_len = struct.pack('<Q', len(request))
        packet = 'ZBXD\x01' + data_len + request
        logger.debug('%s.__create_packet (str): %s', self.cn, packet)
        logger.debug('%s.__create_packet (hex): %s', self.cn,
                     ':'.join(x.encode('hex') for x in packet))

        return packet

    def __get_response(self, connection):
        """
        Get response from zabbix server, reads from self.socket.

        Returns:
          str: JSON response from zabbix server or False in case of some errors
        """

        response_header = self.__receive(connection, 13)
        logger.debug('%s.__get_response.response_header: %s', self.cn, response_header)

        if not response_header.startswith('ZBXD\x01') or len(response_header) != 13:
            logger.debug('%s.__get_response: Wrong zabbix response', self.cn)
            result = False
        else:
            response_len = struct.unpack('<Q', response_header[5:])[0]

            response_body = connection.recv(response_len)

            result = json.loads(response_body)
            logger.debug('%s.__get_response: %s', self.cn, result)

        try:
            connection.close()
        except:
            pass

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
            logger.debug('%s.send(%s): connecting', self.cn, host_addr)

            # create socket object
            connection = socket.socket()

            # server and port must be tuple
            connection.connect(host_addr)

            try:
                connection.sendall(packet)
            except Exception as e:
                logger.debug("%s.send: Error while sending the data to zabbix\nERROR:%s", self.cn, e)
                connection.close()
                exit()

            # socket will be closed in self._get_response()
            response = self.__get_response(connection)
            logger.debug('%s.send(%s): %s', self.cn, host_addr, response)

            if response and response.get('response') == 'success':
                result = True
            else:
                logger.debug('%s.send: Got error from zabbix => %s}', self.cn, response)
                raise Exception('Zabbix Server ({0}) reject packet.'.format(host_addr))

        return result
