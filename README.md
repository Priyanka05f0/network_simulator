# Network Packet Simulator

A professional API tool that simulates network packet flow through a virtual environment. It demonstrates core networking concepts including DNS resolution, Firewall rules, and Routing logic.

## 🚀 Setup Instructions

1. **Install Dependencies**
   Run this command in your terminal:
   ```bash
   pip install -r requirements.txt
2. Start the Server Launch the API with:

uvicorn main:app --reload

The server runs at: http://127.0.0.1:8000
Interactive Docs: http://127.0.0.1:8000/docs
   
***API Documentation***

Endpoint: POST /trace
This is the main endpoint. It accepts a JSON packet definition and returns a hop-by-hop trace of the packet's path.
### Request Parameters (JSON)

| Field | Type | Description |
| :--- | :--- | :--- |
| `src_ip` | string | The IP address sending the packet (e.g., "192.168.1.50") |
| `destination` | string | Target Hostname (e.g., "google.com") or IP address |
| `dest_port` | integer | Target Port (e.g., 80, 443) |
| `protocol` | string | Network Protocol (e.g., "TCP", "UDP") |
| `initial_ttl` | integer | Time-To-Live hop limit (e.g., 64) |

## Example 1: Successful Trace

This simulates a packet that is allowed by the firewall and finds a route to the destination.

Request:
```
JSON
{
  "src_ip": "192.168.1.50",
  "destination": "google.com",
  "dest_port": 443,
  "protocol": "TCP",
  "initial_ttl": 64
}
```
Response:
```
JSON
{
  "status": "success",
  "trace": [
    "DNS Resolved to 8.8.8.8",
    "Firewall Allowed",
    "Routed via 10.0.0.254",
    "TTL Decremented"
  ]
}
```
---
## Example 2: Blocked Traffic (Firewall)

This simulates a packet from a restricted IP (10.0.0.5) trying to access port 80.

Request:
```
JSON
{
  "src_ip": "10.0.0.5",
  "destination": "192.168.1.10",
  "dest_port": 80,
  "protocol": "TCP",
  "initial_ttl": 64
}
```
Response:
```
JSON
{
  "status": "blocked",
  "trace": [
    "DNS Resolved to 192.168.1.10",
    "Firewall Blocked"
  ]
}
```

---

## ⚙️ Configuration
The network topology is defined in `config/scenario-basic.json`.
* **DNS:** Maps hostnames (e.g., `google.com`) to IP addresses.
* **Firewall:** Defined rules for `ALLOW` or `DENY` based on IP/Protocol.
* **Routes:** Defines subnets and gateways using CIDR notation.

## 📂 Project Structure
* `main.py`: The FastAPI server and entry point.
* `src/components.py`: Contains the logic for DNS, Router, and Firewall classes.
* `config/`: Contains the JSON network scenarios.









