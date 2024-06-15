import socket
import ssl
import dns.resolver
import threading
import subprocess

# 1. TCP/IP Communication: Simple TCP Client and Server

# TCP Server
def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("TCP Server listening on port 12345...")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        data = client_socket.recv(1024).decode()
        print(f"Received: {data}")
        client_socket.sendall("Echo: ".encode() + data.encode())
        client_socket.close()

# TCP Client
def tcp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    client_socket.sendall("Hello, Server!".encode())
    data = client_socket.recv(1024).decode()
    print(f"Received from server: {data}")
    client_socket.close()

# 2. DNS Queries
def perform_dns_query(domain):
    resolver = dns.resolver.Resolver()
    answers = resolver.resolve(domain, 'A')
    for ip in answers:
        print(f"{domain} has IP address {ip}")

# 3. Secure Communication with TLS
def secure_tcp_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='server.pem', keyfile='server-key.pem')

    bindsocket = socket.socket()
    bindsocket.bind(('localhost', 12346))
    bindsocket.listen(5)
    print("TLS Server listening on port 12346...")

    while True:
        newsocket, fromaddr = bindsocket.accept()
        connstream = context.wrap_socket(newsocket, server_side=True)
        try:
            data = connstream.recv(1024).decode()
            print(f"Received: {data}")
            connstream.sendall("Secure Echo: ".encode() + data.encode())
        finally:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()

def secure_tcp_client():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('server-cert.pem')

    with socket.create_connection(('localhost', 12346)) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as ssock:
            ssock.sendall("Hello, Secure Server!".encode())
            data = ssock.recv(1024).decode()
            print(f"Received from server: {data}")

# 4. BGP Interaction using ExaBGP
def bgp_announce():
    bgp_config = '''
    neighbor 127.0.0.1 {
        router-id 192.0.2.1;
        local-address 192.0.2.1;
        local-as 65000;
        peer-as 65001;
        static {
            route 203.0.113.0/24 next-hop self;
        }
    }
    '''
    with open('exabgp.conf', 'w') as f:
        f.write(bgp_config)

    # Start ExaBGP with the configuration
    subprocess.Popen(['exabgp', 'exabgp.conf'])

# Example usage
if __name__ == "__main__":
    # Start TCP Server
    threading.Thread(target=tcp_server).start()

    # Start Secure TCP Server
    threading.Thread(target=secure_tcp_server).start()

    # Perform DNS Query
    perform_dns_query("example.com")

    # Start TCP Client
    tcp_client()

    # Start Secure TCP Client
    secure_tcp_client()

    # Announce BGP Route
    bgp_announce()
