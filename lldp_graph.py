#!/usr/bin/python3
from napalm import get_network_driver
import json

# importing driver for cisco
driver = get_network_driver('ios')

# specifying root device from which we will begin to search
root_device = 'cisco1'

# setting lldp devices to an empty list
lldp_devices = []

def get_lldp_neighbors(device):

    local_interfaces = []
    local_neighbors = []
    lldp_device = {}

    # specifying authentication vars
    username = 'admin'
    password = 'admin'
    optional = {'secret': 'admin'}

    # establishing connection parameters
    device_con = driver(device, username, password, optional_args=optional )

    # opening SSH connection
    device_con.open()

    # using napalm to collect lldp neighhbors
    device_facts = device_con.get_lldp_neighbors()

    # close SSH connection
    device_con.close()

    # removing '.testing' domain name from all lldp neighbors collected
    for entry in device_facts:
        for neighbor in device_facts[entry]:
            local_neighbors.append(neighbor['hostname'].replace('.testing', ''))
            local_interfaces.append(entry)
    
    # setting up dict keys
    lldp_device['host'] = device
    lldp_device['neighbors_hostname'] = local_neighbors
    lldp_device['interfaces'] = local_interfaces

    # if device is not already in the list add it
    if device not in lldp_devices:
        lldp_devices.append(lldp_device)

    # return dictionary
    return lldp_device

lldp_devices = [ get_lldp_neighbors(root_device) ]

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
        get_lldp_neighbors(device)

lldp_discovery()

print(json.dumps(lldp_devices, indent=2))