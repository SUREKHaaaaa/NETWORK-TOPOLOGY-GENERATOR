# validator.py - Network Configuration Validation
from models import Device, Interface, Network

def validate_network(network):
    """Run all validation checks on the network."""
    print("\n" + "="*60)
    print("NETWORK VALIDATION REPORT")
    print("="*60)
    
    # Check for duplicate IPs
    print("\n1. Checking for duplicate IP addresses...")
    ip_map = {}
    duplicates_found = False
    for device_name, device in network.devices.items():
        for intf_name, interface in device.interfaces.items():
            if interface.ip_address:
                if interface.ip_address in ip_map:
                    print(f"   ⚠️  DUPLICATE IP: {interface.ip_address}")
                    print(f"      Found on {device_name}({intf_name}) and {ip_map[interface.ip_address]}")
                    duplicates_found = True
                else:
                    ip_map[interface.ip_address] = f"{device_name}({intf_name})"
    if not duplicates_found:
        print("   No duplicate IP addresses found.")
    
    # Check for MTU mismatches
    print("\n2. Checking for MTU mismatches on links...")
    mtu_mismatches = False
    for link in network.links:
        dev1, intf1, dev2, intf2 = link
        mtu1 = network.devices[dev1].interfaces[intf1].mtu
        mtu2 = network.devices[dev2].interfaces[intf2].mtu
        if mtu1 != mtu2:
            print(f"   ⚠️  MTU MISMATCH: {dev1}({intf1})={mtu1} <-> {dev2}({intf2})={mtu2}")
            mtu_mismatches = True
    if not mtu_mismatches:
        print("   No MTU mismatches found.")
    
    # Check for network loops using DFS
    print("\n3. Checking for potential network loops...")
    if has_loops(network):
        print("   ⚠️  POTENTIAL LOOP: Network topology may contain loops")
    else:
        print("   No loops detected.")
    
    # Check for devices with no connections
    print("\n4. Checking for isolated devices...")
    connected_devices = set()
    for link in network.links:
        connected_devices.add(link[0])
        connected_devices.add(link[2])
    
    isolated_devices = []
    for device_name in network.devices:
        if device_name not in connected_devices:
            isolated_devices.append(device_name)
    
    if isolated_devices:
        for device in isolated_devices:
            print(f"   ⚠️  ISOLATED DEVICE: {device} has no connections")
    else:
        print("   No isolated devices found.")
    
    print("\n" + "="*60)
    print("Validation completed!")
    input("Press Enter to return to main menu...")

def has_loops(network):
    """Check if the network graph has cycles using DFS."""
    if not network.links:
        return False
        
    graph = {}
    for link in network.links:
        dev1, dev2 = link[0], link[2]
        if dev1 not in graph:
            graph[dev1] = []
        if dev2 not in graph:
            graph[dev2] = []
        graph[dev1].append(dev2)
        graph[dev2].append(dev1)
    
    visited = set()
    for node in graph:
        if node not in visited:
            if dfs_detect_cycle(graph, node, visited, None):
                return True
    return False

def dfs_detect_cycle(graph, node, visited, parent):
    """DFS helper to detect cycles."""
    visited.add(node)
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            if dfs_detect_cycle(graph, neighbor, visited, node):
                return True
        elif neighbor != parent:
            return True
    return False