# Intelligent Network Topology Generator & Simulator

> Automatically transform raw device configurations into actionable network intelligence.

---

## Overview

Manual network discovery is slow and error-prone. This tool automates the entire process—parsing router/switch configs, building hierarchical topologies, validating configurations, and simulating real-world network behavior—all from a single command-line interface.

---

## Key Capabilities

| Feature | Description |
|---------|-------------|
| **Config Parsing** | Extracts hostnames, IPs, subnets, and bandwidth from `.dump` files |
| **Topology Generation** | Builds bandwidth-aware graphs and exports visual diagrams |
| **Hierarchy Classification** | Auto-detects Core, Distribution, and Access layers |
| **Validation Engine** | Detects duplicate IPs, MTU mismatches, loops, and isolated devices |
| **Day-1 Simulation** | Simulates device boot, ARP discovery, and OSPF neighbor formation |
| **Fault Injection** | Tests link failures and predicts network impact |

---

## Tech Stack

- **Python** – Core logic and orchestration
- **NetworkX** – Graph-based network modeling
- **iGraph** – Topology visualization
- **Regex** – Configuration file parsing


---

## Quick Start

```bash
# 1. Place your config files in the Conf/ folder
# 2. Run the tool
python network_analyzer.py

# 3. Use the interactive menu:
#    [1] Show Topology & Hierarchy
#    [2] Validation Report
#    [3] Day-1 Simulation
#    [4] Fault Injection
#    [5] Exit
