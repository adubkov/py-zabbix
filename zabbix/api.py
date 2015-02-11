import json
import logging
import re
import urllib2

class _NullHandler(logging.Handler):
  """
  Null Handler class for Logger
  """

  def emit(self, record):
    pass

logger = logging.getLogger(__name__)
logger.addHandler(_NullHandler())

class ZabbixAPIException(Exception):
  """
  ZabbixAPI exception class

  code list:
  -32602 - Invalid params (eg already exists)
  -32500 - no permissions
  """
  pass

class ZabbixAPIObjectClass(object):
  """
  ZabbixAPI Object class
  """

  def __init__(self, name, parent):
    self.name = name
    self.parent = parent

  def __getattr__(self, attr):
    """
    Dynamically create a method (ie: get)
    """

    def fn(*args, **kwargs):
      if args and kwargs:
        raise TypeError("Found both args and kwargs")

      logger.debug(attr)

      return self.parent.do_request(
          '{0}.{1}'.format(self.name, attr),
          args or kwargs
      )['result']

    return fn

class ZabbixAPI(object):
  """
  ZabbixAPI class, implement interface to zabbix api

  Examples:
    z = ZabbixAPI('https://zabbix.server', user='admin', password='zabbix')

    # Get API Version
    z.api_info.version()
    >> u'2.2.1'
    # ir
    z.do_request('apiinfo.version')
    >> {u'jsonrpc': u'2.0', u'result': u'2.2.1', u'id': u'1'}

    # Get all disabled hosts
    z.host.getobjects(status=1)
    # or
    z.do_request('host.getobjects', {'status':1})

  """

  def __init__(self, url='https://localhost/zabbix',
               use_authenticate=False, user='admin', password='zabbix'):
    self.use_authenticate = use_authenticate
    self.auth = ''
    self.url = url + '/api_jsonrpc.php'
    self.__login(user, password)
    logger.debug("JSON-PRC Server: %s", self.url)

  def __getattr__(self, attr):
    """
    Dynamically create an object class (ie: host)
    """
    return ZabbixAPIObjectClass(attr, self)

  def __login(self, user='', password=''):
    """
    Do login to zabbix server

    Attributes:
      user (str):     Zabbix user
      password (str): Zabbix user password
    """
    logger.debug("ZabbixAPI.login({0},{1})".format(user, password))

    self.auth = ''

    if self.use_authenticate:
      self.auth = self.user.authenticate(user=user, password=password)
    else:
      self.auth = self.user.login(user=user, password=password)

  def api_version(self):
    """
    Return version of Zabbix API
    """
    return self.apiinfo.version()

  def do_request(self, method, params=None):
    """
    Make request to Zabbix API

    Attributes:
      method (str): Any of ZabbixAPI method, like: apiinfo.version
      params (str): Methods parameters

    Examples:
      z = ZabbixAPI()
      apiinfo = z.do_request('apiinfo.version')
    """
    request_json = {
      'jsonrpc':'2.0',
      'method': method,
      'params': params or {},
      'auth': self.auth,
      'id': '1',
    }

    logger.debug('urllib2.Request({0}, {1})'.format(self.url,json.dumps(request_json)))
    req = urllib2.Request(self.url, json.dumps(request_json))
    req.get_method = lambda: 'POST'
    req.add_header('Content-Type', 'application/json-rpc')

    try:
      res = urllib2.urlopen(req)
      response_json = json.load(res)
    except ValueError:
      raise ZabbixAPIException("Unable to parse json: %" % res)

    logger.debug("Response Body: %s" % json.dumps(response_json, indent=4,
      separators=(',', ': ')))

    if 'error' in response_json:
      msg = "Error {code}: {message}, {data} while sending {json}".format(
        code=response_json['error']['code'],
        message=response_json['error']['message'],
        data=response_json['error']['data'],
        json=str(request_json)
      )
      raise ZabbixAPIException(msg, response_json['error']['code'])

    return response_json

  def get_id(self, item_type, item=None, with_id=False, hostid=None, **args):
    """
    Return id or ids of zabbix objects.

    Attributes:
      item_type   (str): Type of zabbix object
      item        (str): Name of zabbix object.
                         If None - will return list of all object in the scope.
      with_id    (bool): Return values will be in zabbix format.
                         Examlpe: {'itemid: 128}
      hostid      (int): Specify id of host for special cases
      templateid  (int): Specify scope to specific template
      app_name    (str): Specify scope to specific template

    """
    result = None

    type_ = '{item_type}.get'.format(item_type=item_type)

    item_filter_name = {
      'trigger': 'description',
      'triggerprototype': 'description',
      'mediatype': 'description',
      'user': 'alias',
    }

    item_id_name = {
      'usergroup': 'usrgrp',
      'hostgroup': 'group',
      'discoveryrule': 'item',
      'graphprototype': 'graph',
      'itemprototype': 'item',
      'triggerprototype': 'trigger',
    }

    filter_ = { 'filter': { item_filter_name.get(item_type, 'name'): item }, 'output':'extend' }
    if hostid:
      filter_['filter'].update({ 'hostid': hostid })

    if args.get('templateid'):
      filter_['templateids'] = args['templateid']
    if args.get('app_name'):
      filter_['application'] = args['app_name']

    logger.debug('do_request( "{type}", {filter} )'.format(type=type_, filter=filter_))
    response = self.do_request(type_, filter_)['result']

    if response:
      item_id = '{item}id'.format(item=item_id_name.get(item_type, item_type))
      result = []
      for obj in response:
        if with_id:
          result.append({ item_id: int(obj.get(item_id)) })
        else:
          result.append(int(obj.get(item_id)))

      list_types = (list, type(None))
      if not isinstance(item, list_types):
        result = result[0]

    return result
