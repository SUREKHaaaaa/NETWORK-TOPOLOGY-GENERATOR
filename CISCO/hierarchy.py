# hierarchy.py - Hierarchical Network Analysis
from models import Device, Interface, Network
import networkx as nx

def analyze_hierarchy(network):
    """Analyze network and assign Core, Distribution, Access roles."""
    print("Analyzing network hierarchy...")
    
    # Create a graph
    G = nx.Graph()
    
    # Add devices as nodes
    for device_name in network.devices:
        G.add_node(device_name)
    
    # Add links as edges
    for link in network.links:
        G.add_edge(link[0], link[2])
    
    # Assign roles based on network topology
    if G.number_of_nodes() == 0:
        return
    
    try:
        # Calculate centrality to find important nodes
        centrality = nx.betweenness_centrality(G)
        sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        
        # Assign Core role to most central nodes
        for node, _ in sorted_nodes[:min(2, len(sorted_nodes))]:
            network.devices[node].role = "Core"
        
        # Assign Access role to nodes with only one connection
        for node in G.nodes():
            if G.degree(node) == 1:
                network.devices[node].role = "Access"
        
        # Everything else is Distribution
        for device in network.devices.values():
            if device.role == "Unassigned":
                device.role = "Distribution"
                
        print("Hierarchy analysis completed successfully!")
        
    except Exception as e:
        print(f"Note: Using simple hierarchy analysis: {str(e)}")
        # Fallback: assign based on degree
        for device_name in network.devices:
            degree = G.degree(device_name) if device_name in G else 0
            if degree == 1:
                network.devices[device_name].role = "Access"
            elif degree >= 3:
                network.devices[device_name].role = "Core"
            else:
                network.devices[device_name].role = "Distribution"
                