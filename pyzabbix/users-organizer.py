# -*- encoding: utf-8 -*-
#
# Copyright © 2017 Andrey Makarov
#
# This file is user for simple manipulations with users

from pprint import pprint

from pyzabbix import ZabbixAPIException


class UserOrganizer:
    """
    This function gets an object of ZabbixAPI connection to the Zabbix server
    Returns user's id and aliases
    """
    def get_users(z):
        try:
            response = z.do_request(method="user.get", params={
                "filter": "alias",
                "output": ["userid", "alias"]
            })
            result = response['result']
        except ZabbixAPIException as e:
            print(e)
        return result

    """
    This function gets an object of ZabbixAPI connection to the Zabbix server
    Gets user name, must be a string value
    Prints users alias, ip, name, surname, id
    """
    def get_user_info(z, user_name):
        try:
            response = z.do_request(method="user.get", params={
                "search": {"alias": user_name},
                "output": "extend"
            })
        except ZabbixAPIException as e:
            print(e)
        nick_name = response['result'][0]['alias']
        attempt_ip = response['result'][0]['attempt_ip']
        name = response['result'][0]['name']
        surname = response['result'][0]['surname']
        user_id = response['result'][0]['userid']

        pprint("nick name = " + nick_name)
        pprint("ip = " + attempt_ip)
        pprint("name = " + name)
        pprint("surname = " + surname)
        pprint("user id = " + user_id)

    """
    This function gets an object of ZabbixAPI connection to the Zabbix server
    Gets user name, must be a string value
    Returns user's maps
    """
    def get_user_maps(z, user_name):
        id = z.get_user_id(user_name)
        try:
            response = z.do_request(method="map.get", params={
                "output": ["label"],
                "userids": id
            })
        except ZabbixAPIException as e:
            print(e)
        return response

    """
    This function gets an object of ZabbixAPI connection to the Zabbix server
    Gets user name, must be a string value
    Returns user's id
    """
    def get_user_id(z, user_name):
        try:
            response = z.do_request(method="user.get", params={
                "search": {"alias": user_name},
                "output": "extend"
            })
        except ZabbixAPIException as e:
            print(e)
        return response['result'][0]["userid"]