#!/usr/bin/python3

from napalm import get_network_driver
import json

driver = get_network_driver('ios')

#devices = ['192.168.1.1', '192.168.1.2']

device = 'cisco1'

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
            local_neighbors.append(neighbor['hostname'].replace('.testing', ''))
            local_interfaces.append(entry)
    
    lldp_device['host'] = device
    lldp_device['neighbors_hostname'] = local_neighbors
    lldp_device['interfaces'] = local_interfaces

    if device not in lldp_devices:
        lldp_devices.append(lldp_device)

    return lldp_device

lldp_devices = [ get_lldp_neigh(device) ]

def lldp_discovery():

    all_lldp_names = []

    for router in range(len(lldp_devices)):
        rtr_name = lldp_devices[router]['neighbors_hostname']
        all_lldp_names.append(rtr_name)
        print(all_lldp_names)

lldp_discovery()