# -*- encoding: utf-8 -*-
#
# Copyright © 2017 Andrey Makarov
#
# This file is user for simple manipulations with hosts
from pprint import pprint

from pyzabbix import ZabbixAPIException


class HostsOrganizer:

    """
    This function gets an object of ZabbixAPI connection to the Zabbix server
    Gets template id, host id, must be a string value
    Used for setting template on host
    """
    def add_template_on_host(z, template_id, host_id):
        try:
            response = z.do_request(method="template.massadd", params={
                "templates": [
                    {
                        "templateid": template_id
                    }
                ],
                "hosts": [
                    {
                        "hostid": host_id
                    },
                ]
            })
            pprint(response)
        except ZabbixAPIException as e:
            print(e)

    """
    This function gets an object of ZabbixAPI connection to the Zabbix server
    Gets hosts group's id, must be a string value
    Returns list of duplicates
    """
    def search_hosts_duplicates(z, group_id):
        ids = z.do_request(method="host.get", params={
            "output": ["hostid"],
            "filter": {
                "groupids": group_id
            }
        })

        ips = []
        duplicates = []
        for i, host in enumerate(ids['result']):
            try:
                response = z.do_request(method="hostinterface.get", params={
                    "output": ["ip", "hostid"],
                    "hostids": host['hostid']
                })
            except ZabbixAPIException as e:
                print(e)
            else:
                ip = response['result'][0]['ip']
                if ip in ips:
                    duplicates.append({
                        'ip': ip,
                        'id': response['result'][0]['hostid']
                    })
                else:
                    ips.append(ip)
        return duplicates

    """
    This function gets an object of ZabbixAPI connection to the Zabbix server
    Gets template id, group id, must be a string value
    Used for setting template on group
    """
    def add_template_on_group(z, template_id, group_id):
        icmp_ping = "10104"
        try:
            response = z.do_request(method="template.massadd", params={
                "templates": [
                    {
                        "templateid": template_id
                    }
                ],
                "groups": [
                    {
                        "groupid": group_id
                    }
                ]
            })
            pprint(response)
        except ZabbixAPIException as e:
            print(e)