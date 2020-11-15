#!/usr/bin/python3
from napalm import get_network_driver
import matplotlib
import networkx
from pprint import pprint

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
    lldp_devices_needing_query = []

    # Looping over current list of devices
    for router in range(len(lldp_devices)):
        # making rtr_name to be the hostname of each neighbor
        rtr_name = lldp_devices[router]['neighbors_hostname']
        # append the rtr_name to the list
        all_lldp_names.append(rtr_name)

    # looping over all device names
    for device in all_lldp_names[0]:
        # loop over global device list
        for current_lldp_devices in lldp_devices:
            # determining if device is not in list
            if device != current_lldp_devices['host']:
                lldp_devices_needing_query.append(device)

    for device in lldp_devices_needing_query:
        get_lldp_neighbors(device)

def non_direct_discovery():
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

def formatting_lldp_list():
    formatted_neighbors = {}

    for device in lldp_devices:
        for index, neighbor in enumerate(device['neighbors_hostname']):
            # Creating a tuple with host and neighbor connection
            every_tuple = (device['host'], device['neighbors_hostname'][index])
            # for every tuple adding in interface connection
            formatted_neighbors[every_tuple] = device['interfaces'][index]

    return formatted_neighbors

def generate_graph(neighborships):

    # inititate empty graph
    G = networkx.Graph()

    # use the tuples to form the edges
    G.add_edges_from(neighborships.keys(), weight=3)

    # laying out a spring layout
    pos = networkx.spring_layout(G, k=0.1, iterations=70)

    # setting the labels
    networkx.draw_networkx_labels(G, pos, font_size=9, font_family='sans-serif', font_weight='bold')

    # Choosing width and edge_color
    networkx.draw_networkx_edges(G, pos, width=5, alpha=1.0, edge_color='blue')
    # Setting our edge labels
    networkx.draw_networkx_edge_labels(G, pos, neighborships, label_pos=0.3, font_size=8)

    # Drawing the graph
    networkx.draw(G, pos, node_size=2000, with_labels=False, edgecolors='black')
    
    # set the function to return a graph
    return matplotlib.pyplot.show()

def main():
    # specifying root device from which we will begin to search
    root_device = input("What is the root device name or ip? ")
    
    # setting lldp devices to an empty list and setting it to be in the global namespace
    global lldp_devices
    lldp_devices = []

    # converting each entry to an item in a list
    lldp_devices = [ get_lldp_neighbors(root_device) ]

    # execute lldp_discovery
    lldp_discovery()

    # execute extended function to find not directly connected neighbors
    non_direct_discovery()

    lldp_devices = formatting_lldp_list()

    pprint(lldp_devices)

    generate_graph(lldp_devices)

if __name__ == '__main__':
    main()