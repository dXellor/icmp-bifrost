import pathlib
import socket 
import struct

def convert_ip_address_to_bytes(ip: str) -> bytes:
    return socket.inet_aton( ip )

def convert_bytes_to_ip_address(bytes: bytes) -> str:
    return socket.inet_ntoa( bytes )

def get_iptables_script_path(script_name: str) -> str:
    src_dir = pathlib.Path( __file__ ).parent.parent.resolve()
    return pathlib.Path( src_dir, 'scripts', script_name ).resolve()

def calculate_ip_header_checksum(packet: bytearray) -> bytes:
    header_len = ( packet[0] & 0xF )
    checksum_packet = packet[0 : header_len]
    checksum_packet[10:12] = 0x0000.to_bytes()

    return calculate_checksum( checksum_packet )

def calculate_tcp_header_checksum(packet: bytearray) -> bytes:
    ip_header_len = ( packet[0] & 0xF )
    tcp_packet = packet[ip_header_len : ]
    tcp_packet[16:18] = 0x0000.to_bytes()

    checksum_packet = bytearray()
    checksum_packet.append( packet[12:16] )
    checksum_packet.append( packet[16:20] )
    checksum_packet.append( 0x00.to_bytes() )
    checksum_packet.append( ( packet[8] & 0xF ).to_bytes() )
    checksum_packet.append( tcp_packet )
    return calculate_checksum( checksum_packet )

def calculate_checksum(checksum_packet: bytearray) -> bytes:
    packet = bytes( checksum_packet )

    checksum_result = 0
    for i in range( 0, len( packet ), 2 ):
        checksum_result += ( packet[i] << 8 ) + ( struct.unpack( 'B', packet[i + 1:i + 2] )[0] if len( packet[i + 1:i + 2] ) else 0 )

    checksum_result = ( checksum_result >> 16 ) + ( checksum_result & 0xFFFF )
    checksum_result += ( checksum_result >> 16 )
    checksum_result = ~checksum_result & 0xFFFF
    return checksum_result.to_bytes()