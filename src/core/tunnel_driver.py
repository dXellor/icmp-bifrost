from netfilterqueue import NetfilterQueue, Packet
import socket
import subprocess
import sys

from .icmp_packet import ICMPPacket
from utils.enums import Modes, Marks, ExitCodes
from utils.network import *

class TunnelDriver:

    def __init__(self, destination: str, mode: Modes) -> None:
        self.mode = mode
        self.icmp_socket = None
        self.raw_socket = None
        self.destination = destination
        self.source = socket.gethostbyname( socket.gethostname() )
        
        self.open_icmp_sockets()

    def open_icmp_sockets(self) -> None:
        try:
            self.icmp_socket = socket.socket( socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP )
            self.raw_socket = socket.socket( socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW )
        except socket.error as e:
            print(f"Error while initializing sockets: {e}")
            sys.exit(ExitCodes.CANT_OPEN_SOCKET)

    def setup_iptables_rules(self) -> None:
        if self.mode == Modes.CLIENT:
            script_exit_code = subprocess.call( ['bash', get_iptables_script_path('setup_iptables_client.sh'), self.source, self.destination] )
        else:
            script_exit_code = subprocess.call( ['bash', get_iptables_script_path('setup_iptables_server.sh'), self.destination, self.source] )

        if script_exit_code != 0:
            print( "Unable to setup iptable rules" )
            self.clear_iptables_rules()
            exit( ExitCodes.IPTABLES_SETUP_ERROR )

    def clear_iptables_rules(self) -> None:
        if self.mode == Modes.CLIENT:
            subprocess.call( ['bash', get_iptables_script_path('clear_iptables.sh'), self.source, self.destination] )
        else:
            subprocess.call( ['bash', get_iptables_script_path('clear_iptables.sh'), self.destination, self.source] )

    def run(self):
        self.setup_iptables_rules()

        nfqueue = NetfilterQueue()
        nfqueue.bind(1, self.handle_queue)
        try:
            nfqueue.run()
        except KeyboardInterrupt:
            print('')

        self.clear_iptables_rules()
        nfqueue.unbind()

    def handle_queue(self, packet: Packet) -> None:
 
        if packet.get_mark() == Marks.TO_SERVER or packet.get_mark() == Marks.TO_CLIENT:
            self.wrap_icmp_and_send( packet )
            return

        if packet.get_mark() == Marks.FROM_CLIENT or packet.get_mark() == Marks.FROM_SERVER:
            self.unwrap_icmp_and_recieve( packet )
            return

        packet.accept()

    def wrap_icmp_and_send(self, packet: Packet) -> None:
        icmp_packet = ICMPPacket( self.destination, packet.get_mark() == Marks.TO_CLIENT )
        ip_header_len = ( packet.get_payload()[0] & 0xF )
        secret_payload = bytearray( packet.get_payload() )

        if packet.get_mark() == Marks.TO_CLIENT:
            secret_payload[16:20] = convert_ip_address_to_bytes( self.destination )
            secret_payload[10:12] = calculate_ip_header_checksum( secret_payload )
            secret_payload[ip_header_len + 16: ip_header_len + 18] = calculate_tcp_header_checksum( secret_payload )

        icmp_packet.payload = secret_payload
        self.icmp_socket.sendto( icmp_packet.get_raw(), ( self.destination, 1001 ))
        packet.drop()

    def unwrap_icmp_and_recieve(self, packet: Packet) -> None:
        raw_icmp = packet.get_payload()
        ip_header_len = ( raw_icmp[0] & 0xF )
        ip_and_icmp_header_len = ip_header_len + 8
        secret_payload = bytearray( raw_icmp[ip_and_icmp_header_len + 8:] )

        if packet.get_mark() == Marks.FROM_CLIENT:
            secret_payload[12:16] = convert_ip_address_to_bytes( self.source )
            secret_payload[10:12] = calculate_ip_header_checksum( secret_payload )
            secret_payload[ip_header_len + 16: ip_header_len + 18] = calculate_tcp_header_checksum( secret_payload )
            packet_destination = convert_bytes_to_ip_address( secret_payload[16:20] )
        else:
            packet_destination = self.source

        # packet.set_payload( bytes( secret_payload ) )
        self.raw_socket.sendto( bytes(secret_payload), ( packet_destination, 0 ) )
        packet.drop()