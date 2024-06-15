
# Network Tools

This repository contains a Python script that showcases fundamental networking concepts including TCP/IP communication, DNS querying, secure TLS communication, and BGP interaction using ExaBGP.

## Features

- **TCP/IP Communication**: Simple TCP client and server.
- **DNS Queries**: Perform DNS A record lookups.
- **Secure Communication**: TLS-encrypted TCP client and server.
- **BGP Interaction**: Announce BGP routes using ExaBGP.

## Usage

1. **Install Dependencies**:
   ```bash
   pip install dnspython exabgp
   ```

2. **Run the Script**:
   ```bash
   python network_tools.py
   ```

3. **Ensure TLS Certificates**:
   Place `server.pem`, `server-key.pem`, and `server-cert.pem` in the script directory.

