#!/usr/bin/python3

from napalm import get_network_driver
import json

driver = get_network_driver('ios')

#devices = ['192.168.1.1', '192.168.1.2']

device = '192.168.1.1'

lldp_devices = []

def get_lldp_neigh(ip):

    local_interfaces = []
    local_neighbors = []
    lldp_device = {}

    username = 'admin'
    password = 'admin'
    optional = {'secret': 'admin'}

    device_con = driver(device, username, password, optional_args=optional )

    device_con.open()

    device_facts = device_con.get_lldp_neighbors()

    device_con.close()

    for entry in device_facts:
        for neighbor in device_facts[entry]:
            local_neighbors.append(neighbor['hostname'])
            local_interfaces.append(entry)
    
    lldp_device['Host'] = device
    lldp_device['neighbors_name'] = local_neighbors
    lldp_device['interfaces'] = local_interfaces

    if device not in lldp_devices:
        lldp_devices.append(lldp_device)

    return lldp_device

print(get_lldp_neigh(device))