#!/usr/bin/python3
from napalm import get_network_driver
import json

def get_lldp_neighbors(device):

    local_interfaces = []
    local_neighbors = []
    lldp_device = {}
    
    # importing driver for cisco
    driver = get_network_driver('ios')
    
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

def extend_neighbor_discovery():
    all_devices = []
    all_discovered_neighbors = []

    # collecting all current devices
    for device in lldp_devices:
        all_devices.append(device['neighbors_hostname'])

    # Creating a seperate list for all neighbors of each host
    for discovered_device in lldp_devices:
        all_discovered_neighbors.append(discovered_device['host'])
    
    # flatten list to be a single list
    all_devices = [ item for sublist in all_devices for item in sublist ]

    # removing duplicates
    all_devices = list(set(all_devices))
    
    # executing get_lldp_neighbors function if there are undiscovered neighbors
    for device in all_devices:
        if device not in all_discovered_neighbors:
            get_lldp_neighbors(device)

def main():
    # specifying root device from which we will begin to search
    root_device = 'cisco4'
    
    # setting lldp devices to an empty list and setting it to be in the global namespace
    global lldp_devices
    lldp_devices = []

    # converting each entry to an item in a list
    lldp_devices = [ get_lldp_neighbors(root_device) ]

    # execute lldp_discovery
    lldp_discovery()

    # execute extended function to find not directly connected neighbors
    extend_neighbor_discovery()

    print(json.dumps(lldp_devices, indent=2))

if __name__ == '__main__':
    main()