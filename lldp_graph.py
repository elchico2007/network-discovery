#!/usr/bin/python3

from napalm import get_network_driver
import json

driver = get_network_driver('ios')

#devices = ['192.168.1.1', '192.168.1.2']

device = 'cisco1'

lldp_devices = []

def get_lldp_neigh(device):

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

    #print(lldp_devices)

    if device not in lldp_devices:
        lldp_devices.append(lldp_device)

    return lldp_device

lldp_devices = [ get_lldp_neigh(device) ]

def lldp_discovery():

    all_lldp_names = []

    for router in range(len(lldp_devices)):
        rtr_name = lldp_devices[router]['neighbors_hostname']
        all_lldp_names.append(rtr_name)
    
    lldp_devices_needing_query = []

    for device in all_lldp_names[0]:
        for current_lldp_devices in lldp_devices:
            if device != current_lldp_devices['host']:
                lldp_devices_needing_query.append(device)

    for device in lldp_devices_needing_query:
        for current_device in range(len(lldp_devices)):
            for index, entry in enumerate(lldp_devices[current_device]['neighbors_hostname']):
                if device != entry:
                    new_dev_to_query = lldp_devices[current_device]['neighbors_hostname'][index]
                    get_lldp_neigh(new_dev_to_query)
                else:
                    pass
    all_devices = []

    for device in lldp_devices:
        if device not in all_devices:
            all_devices.append(device)

    return all_devices

lldp_discovery()

print(lldp_devices)