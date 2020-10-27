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
    lldp_devices = {}

    username = 'admin'
    password = 'admin'
    optional = {'secret': 'admin'}

    device_con = driver(device, username, password, optional_args=optional )

    device_con.open()

    device_facts = device_con.get_lldp_neighbors()

    for entry in device_facts:
        for neighbor in device_facts[entry]:
            print(neighbor)

    device_con.close()

    print(json.dumps(device_facts, indent=2))

get_lldp_neigh(device)

