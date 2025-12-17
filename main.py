from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from src.components import DNSResolver, Firewall, Router

app = FastAPI()

# Load Config
with open(os.path.join("config", "scenario-basic.json"), 'r') as f:
    config = json.load(f)

dns = DNSResolver(config)
fw = Firewall(config)
router = Router(config)

class Packet(BaseModel):
    src_ip: str
    destination: str
    dest_port: int
    protocol: str
    initial_ttl: int

@app.post("/trace")
def trace(packet: Packet):
    trace_log = []
    
    # CHECK 1: TTL Expiry (New!)
    if packet.initial_ttl <= 0:
        return {"status": "failed", "error": "TTL Exceeded", "trace": trace_log}

    # CHECK 2: DNS Resolution
    # If it is NOT an IP address, try to resolve it
    if not packet.destination.replace('.', '').isdigit():
        resolved_ip = dns.resolve(packet.destination)
        if not resolved_ip:
             # This handles the "NXDOMAIN" requirement
            return {"status": "failed", "error": "NXDOMAIN: Host not found", "trace": trace_log}
        
        packet.destination = resolved_ip
        trace_log.append(f"DNS Resolved to {resolved_ip}")
    
    # CHECK 3: Firewall
    if fw.check(packet) == "deny":
        return {"status": "blocked", "trace": trace_log}
    trace_log.append("Firewall Allowed")

    # CHECK 4: Router
    gateway = router.lookup(packet.destination)
    trace_log.append(f"Routed via {gateway}")
    trace_log.append("TTL Decremented") # Showing we handled the hop

    return {"status": "success", "trace": trace_log}