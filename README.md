# network-discovery
To run the script, clone the repo and use your python 3 interpreter to run the lldp_graph.py file.
You will then be prompted to input a root device to begin the discovery. This will subsequently connect to other
neighbors and attempt to then do a discovery for them.

## Environment
Ensure that you have the following packages installed
```
python3 -m pip install -r requirements.txt
```
## GNS3 physical layout
![Physical GNS3 layout](https://raw.githubusercontent.com/elchico2007/network-discovery/main/python_discovery_physical.PNG)

## Script generated graph
![generated graph](https://raw.githubusercontent.com/elchico2007/network-discovery/main/lldp_neighbors_graph.png)
