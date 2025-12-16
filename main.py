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

    # 1. DNS
    resolved_ip = dns.resolve(packet.destination)
    if resolved_ip:
        packet.destination = resolved_ip
        trace_log.append(f"DNS Resolved to {resolved_ip}")

    # 2. Firewall
    if fw.check(packet) == "deny":
        return {"status": "blocked", "trace": trace_log}
    trace_log.append("Firewall Allowed")

    # 3. Router
    gateway = router.lookup(packet.destination)
    trace_log.append(f"Routed via {gateway}")

    return {"status": "success", "trace": trace_log}