# config_parser.py - Configuration File Parser
from models import Device, Interface, Network
import os
import re
import ipaddress

def parse_configs(network, config_dir):
    """Parse all configuration files in the given directory."""
    print("Parsing configuration files...")
    
    for item in os.listdir(config_dir):
        device_path = os.path.join(config_dir, item)
        if os.path.isdir(device_path):
            config_file = os.path.join(device_path, "config.dump")
            if os.path.isfile(config_file):
                parse_single_config(network, item, config_file)

def parse_single_config(network, device_name, config_path):
    """Parse a single configuration file."""
    device = Device(device_name)
    network.devices[device_name] = device
    
    try:
        with open(config_path, 'r') as f:
            config_text = f.read()
        
        # Find all interface sections
        interface_pattern = r'interface (\S+)\n(.*?)(?=\ninterface|\n\!|\Z)'
        interfaces = re.findall(interface_pattern, config_text, re.DOTALL)
        
        for intf_name, intf_config in interfaces:
            interface = Interface(intf_name)
            
            # Find IP address and mask
            ip_match = re.search(r'ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)', intf_config)
            if ip_match:
                interface.ip_address = ip_match.group(1)
                interface.subnet_mask = ip_match.group(2)
            
            # Find bandwidth
            bw_match = re.search(r'bandwidth (\d+)', intf_config)
            if bw_match:
                interface.bandwidth = int(bw_match.group(1))
            
            device.interfaces[intf_name] = interface
            
        print(f"  - Parsed {device_name} successfully")
        
    except Exception as e:
        print(f"  - Error parsing {device_name}: {str(e)}")

def build_links(network):
    """Build links between devices based on IP addresses and subnets."""
    print("Building network links...")
    
    # Create a list of all interfaces with IP addresses
    all_interfaces = []
    for device_name, device in network.devices.items():
        for intf_name, interface in device.interfaces.items():
            if interface.ip_address and interface.subnet_mask:
                all_interfaces.append((device_name, intf_name, interface))
    
    # Find interfaces on the same subnet and create links
    for i, (dev1, intf1, iface1) in enumerate(all_interfaces):
        for j, (dev2, intf2, iface2) in enumerate(all_interfaces[i+1:], i+1):
            if are_on_same_subnet(iface1.ip_address, iface2.ip_address, iface1.subnet_mask):
                network.links.append((dev1, intf1, dev2, intf2))
                iface1.connected_to = (dev2, intf2)
                iface2.connected_to = (dev1, intf1)
                print(f"  - Link found: {dev1}({intf1}) <-> {dev2}({intf2})")

def are_on_same_subnet(ip1, ip2, mask):
    """Check if two IP addresses are on the same subnet using ipaddress module."""
    try:
        network1 = ipaddress.IPv4Network(f"{ip1}/{mask}", strict=False)
        network2 = ipaddress.IPv4Network(f"{ip2}/{mask}", strict=False)
        return network1 == network2
    except:
        return False