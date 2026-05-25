# network_analyzer.py - Main CLI Menu and Program Flow
from models import Device, Interface, Network
from config_parser import parse_configs, build_links
from hierarchy import analyze_hierarchy
import os
import networkx as nx

def generate_topology_diagram(network):
    """Generates and displays a network topology diagram using igraph."""
    print("\nGenerating Topology Diagram...")
    try:
        import igraph as ig
    except ImportError:
        print("Error: The 'igraph' library is not installed.")
        print("Please run: pip install python-igraph")
        return

    # Create a graph
    G = ig.Graph()
    
    # Add devices as vertices (nodes)
    device_list = list(network.devices.keys())
    G.add_vertices(len(device_list))
    G.vs["name"] = device_list  # Set vertex names
    
    # Add links as edges
    edge_list = []
    for link in network.links:
        device1, device2 = link[0], link[2]
        idx1 = device_list.index(device1)
        idx2 = device_list.index(device2)
        edge_list.append((idx1, idx2))
    
    G.add_edges(edge_list)
    
    # Assign visual properties based on role
    role_colors = {'Core': 'red', 'Distribution': 'blue', 'Access': 'green', 'Unassigned': 'gray'}
    visual_style = {}
    visual_style["vertex_size"] = 30
    visual_style["vertex_label"] = G.vs["name"]  # Use the vertex names as labels
    visual_style["vertex_color"] = [role_colors[network.devices[name].role] for name in device_list]
    visual_style["layout"] = G.layout("kk")  # Kamada-Kawai layout algorithm
    visual_style["bbox"] = (600, 400)  # Size of the image
    visual_style["margin"] = 50
    
    # Plot the graph
    plot = ig.plot(G, **visual_style)
    plot.save("network_topology.png")  # Save the diagram
    print("Diagram successfully saved as 'network_topology.png'")

def run_day1_simulation(network):
    """Simulates basic Day-1 network activities."""
    print("\n=== Day-1 Simulation Started ===")
    input("Press Enter to simulate device boot-up...")
    
    print("\n1. Devices powering on...")
    for device_name in network.devices:
        print(f"   - {device_name} is now online.")
    
    input("\nPress Enter to start ARP Discovery...")
    print("\n2. ARP Discovery Process:")
    print("   - S1: Broadcasting ARP Request: 'Who has 192.168.1.1? Tell 192.168.1.100'")
    print("   - R1: Replying with MAC address: aa:bb:cc:00:11:22")
    
    input("\nPress Enter to start OSPF Discovery...")
    print("\n3. OSPF Neighbor Discovery:")
    print("   - R1: Sending OSPF Hello packet on GigabitEthernet0/0")
    print("   - R2: Received Hello, adjacency forming...")
    print("   - R1 and R2 are now OSPF neighbors!")
    
    input("\nPress Enter to return to main menu...")

def fault_injection_menu(network):
    """Menu for injecting and simulating faults."""
    print("\n=== Fault Injection Menu ===")
    if not network.links:
        print("No links found to break.")
        return
    
    print("Select a link to break:")
    for i, link in enumerate(network.links, 1):
        print(f"{i}. {link[0]} ({link[1]}) <--> {link[2]} ({link[3]})")
    
    try:
        choice = int(input("\nEnter your choice (number): "))
        if 1 <= choice <= len(network.links):
            broken_link = network.links[choice-1]
            print(f"\n*** Simulating failure of link: {broken_link[0]} <--> {broken_link[2]} ***")
            print("Impact Analysis:")
            print("- OSPF recalculating routing paths...")
            print("- Some endpoints may lose connectivity")
            print("- Traffic rerouting through alternative paths")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")
    
    input("\nPress Enter to return to main menu...")

def main():
    """Main function to run the network analyzer."""
    print("Initializing Intelligent Network Analyzer...")
    
    # Create network model
    network = Network()
    
    # Find and parse config files
    config_dir = "Conf"
    if not os.path.exists(config_dir):
        print(f"Error: Directory '{config_dir}' not found. Please create it and add config files.")
        return
    
    parse_configs(network, config_dir)
    build_links(network)
    
    if not network.devices:
        print("No devices found. Please check your config files.")
        return
    
    analyze_hierarchy(network)
    
    # Main menu loop
    while True:
        print("\n" + "="*50)
        print("INTELLIGENT NETWORK TOPOLOGY ANALYZER")
        print("="*50)
        print("1. Show Topology & Hierarchy")
        print("2. Show Validation Report")
        print("3. Run Day-1 Simulation")
        print("4. Inject a Fault")
        print("5. Exit")
        print("="*50)
        
        choice = input("Please choose an option [1-5]: ").strip()
        
        if choice == '1':
            generate_topology_diagram(network)
        elif choice == '2':
            from validator import validate_network
            validate_network(network)
        elif choice == '3':
            run_day1_simulation(network)
        elif choice == '4':
            fault_injection_menu(network)
        elif choice == '5':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()