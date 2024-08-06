import socket 

def get_source_ip_address_in_bytes() -> bytes:
    ip = socket.gethostbyname( socket.gethostname() )
    return socket.inet_aton( ip )