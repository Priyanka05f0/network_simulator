
# Network Packet Simulator

A backend API that simulates the journey of a network packet through a configurable virtual network. This project demonstrates core networking concepts including DNS resolution, Firewall filtering, and IP Routing using the "Longest Prefix Match" algorithm.

## 🛠️ Setup & Installation

**1. Prerequisites**
* Python 3.10 or higher.
* Git (for version control).

**2. Install Dependencies**
Open a terminal in the project folder and run:
```bash
pip install -r requirements.txt

***API Documentation***

Endpoint: POST /trace
This is the main endpoint. It accepts a JSON packet definition and returns a hop-by-hop trace of the packet's path.
***Request Parameters (JSON)***
Field            	Type        	Description
---
src_ip           	string      	The IP address sending the packet (e.g., "192.168.1.50")
destination     	string	      Target Hostname (e.g., "https://www.google.com/url?sa=E&source=gmail&q=google.com") or IP address
dest_port       	integer      	Target Port (e.g., 80, 443)
protocol	        string	      Network Protocol (e.g., "TCP", "UDP")
initial_ttl     	integer	      Time-To-Live hop limit (e.g., 64)

***Example 1: Successful Trace***
This simulates a packet that is allowed by the firewall and finds a route to the destination.

Request:
JSON
{
  "src_ip": "192.168.1.50",
  "destination": "google.com",
  "dest_port": 443,
  "protocol": "TCP",
  "initial_ttl": 64
}

Response:
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
---
***Example 2: Blocked Traffic (Firewall)***
This simulates a packet from a restricted IP (10.0.0.5) trying to access port 80.

Request:
JSON
{
  "src_ip": "10.0.0.5",
  "destination": "192.168.1.10",
  "dest_port": 80,
  "protocol": "TCP",
  "initial_ttl": 64
}

Response:
JSON
{
  "status": "blocked",
  "trace": [
    "DNS Resolved to 192.168.1.10",
    "Firewall Blocked"
  ]
}







