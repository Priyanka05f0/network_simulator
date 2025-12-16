import ipaddress

class DNSResolver:
    def __init__(self, config):
        self.records = config.get('dns', {})
    def resolve(self, hostname):
        if hostname in self.records:
            return self.records[hostname]['value']
        return None

class Firewall:
    def __init__(self, config):
        self.rules = config.get('firewall', [])
    def check(self, packet):
        # Simple check logic for the demo
        for rule in self.rules:
            if rule['src_ip'] == packet.src_ip and rule['action'] == 'deny':
                return "deny"
        return "allow"

class Router:
    def __init__(self, config):
        self.routes = config.get('routes', [])
    def lookup(self, dest_ip):
        return "10.0.0.254" # Default gateway for demo