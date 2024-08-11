import pathlib
import socket 

def convert_ip_address_to_bytes(ip: str) -> bytes:
    return socket.inet_aton( ip )

def convert_bytes_to_ip_address(bytes: bytes) -> str:
    return socket.inet_ntoa( bytes )

def get_iptables_script_path(script_name: str) -> str:
    src_dir = pathlib.Path( __file__ ).parent.parent.resolve()
    return pathlib.Path( src_dir, 'scripts', script_name ).resolve()