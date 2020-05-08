# -*- encoding: utf-8 -*-
#
# Copyright © 2017 Andrey Makarov
#
# This file is user for simple manipulations with hosts's maps

from pprint import pprint

from pyzabbix import ZabbixAPIException


class MapsOrganizer:
    """
    This function gets an object of ZabbixAPI connection to the Zabbix server
    Gets user name, must be a string value
    Returns list with user's maps with map's labels and ids
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

    """
    This function gets an object of ZabbixAPI connection to the Zabbix server
    Gets maps id, must be a string value
    Get's label's text, must be a string value
    Used for changing label's value
    """
    def change_elements_label(z, sysmapid, label):
        for id in sysmapid:
            # pprint(sysmapid)
            new_request = []
            try:
                response = z.do_request(method="map.get", params={
                    "sysmapids": id,
                    "selectSelements": "extend",
                    "output": "extend"
                })['result'][0]['selements']

                # pprint(response)

                for item in response:
                    item["label"] = label
                    new_request.append(item)
                    # pprint(new_request)

            except ZabbixAPIException as e:
                print(e)
            else:
                try:
                    resp = z.do_request(method="map.update", params={
                        "sysmapid": id,
                        "selements": new_request,
                    })
                except ZabbixAPIException as e:
                    print(e, id)

                    def get_sysmapid():
                        ids = []
                        try:
                            response = z.do_request(method="map.get", params={
                                "output": "extends"
                            })
                            for id in response['result']:
                                i = id['sysmapid']
                                ids.append(i)
                        except ZabbixAPIException as e:
                            print(e)
                            return []
                        else:
                            return ids

    """
    This function gets an object of ZabbixAPI connection to the Zabbix server
    Gets map's id, must be a string value
    Get's returned element such as links
    Returns map's elements
    """
    def get_elements(z, sysmapid, returned_element):
        try:
            response = z.do_request(method="map.get", params={
                "sysmapids": sysmapid,
                "output": "extend",
                "selectSelements": "extend",
                "selectLinks": "extend",
                "selectUsers": "extend",
                "selectUserGroups": "extend",
                "selectShapes": "extend",
                "selectLines": "extend"
            })

            # pprint(response['result'][0]['links'])

        except ZabbixAPIException as e:
            print(e)
        return response['result'][0][returned_element]

    """
    This function gets an object of ZabbixAPI connection to the Zabbix server
    Gets map's id, must be a string value
    Get's label type, must be a string value
    Used for changing label type
    """
    def change_label_type(z, sysmapid, label_type):
        for id in sysmapid:
            # pprint(sysmapid)
            new_request = []
            try:
                response = z.do_request(method="map.get", params={
                    "sysmapids": id,
                    "output": "extend"
                })['result'][0]['label_type']

                # pprint(response)

                for item in response:
                    item = label_type
                    new_request.append(item)
                    # pprint(new_request)

            except ZabbixAPIException as e:
                print(e)
            else:
                try:
                    resp = z.do_request(method="map.update", params={
                        "sysmapid": id,
                        "selements": new_request,
                    })
                except ZabbixAPIException as e:
                    print(e)