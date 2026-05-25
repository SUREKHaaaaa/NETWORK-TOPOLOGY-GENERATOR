# models.py - Data models for the network analyzer

class Device:
    def __init__(self, hostname):
        self.hostname = hostname
        self.interfaces = {}
        self.role = "Unassigned"

class Interface:
    def __init__(self, name):
        self.name = name
        self.ip_address = None
        self.subnet_mask = None
        self.bandwidth = None
        self.mtu = 1500
        self.connected_to = None

class Network:
    def __init__(self):
        self.devices = {}
        self.links = []