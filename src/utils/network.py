import socket 

def convert_ip_address_to_bytes(ip: str) -> bytes:
    return socket.inet_aton( ip )