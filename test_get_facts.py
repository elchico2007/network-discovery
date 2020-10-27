#!/usr/bin/python3

from napalm import get_network_driver
import json

devices = ['192.168.1.1', '192.168.1.2']

driver = get_network_driver("ios")

device_facts = []

for device in devices:
    
    device_con = driver(device, 'admin', 'admin', optional_args={'secret': 'admin'} )
    
    device_con.open()
    
    device_facts.append( { device: device_con.get_facts() } )
    
    device_con.close()

print(json.dumps(device_facts, indent=2))
