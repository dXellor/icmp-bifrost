from netfilterqueue import NetfilterQueue, Packet
import socket
import subprocess
import sys

from .icmp_packet import ICMPPacket
from utils.enums import Modes, Marks, ExitCodes
from utils.network import convert_ip_address_to_bytes

class TunnelDriver:

    def __init__(self, destination: str, mode: Modes) -> None:
        self.mode = mode
        self.icmp_socket = None
        self.destination = destination
        self.source = socket.gethostbyname( socket.gethostname() )
        
        self.open_icmp_socket()

    def open_icmp_socket(self) -> None:
        try:
            self.icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except socket.error as e:
            print(f"Error while initializing ICMP socket: {e}")
            sys.exit(ExitCodes.CANT_OPEN_SOCKET)

    def setup_iptables_rules(self) -> None:
        if self.mode == Modes.CLIENT:
            script_exit_code = subprocess.call( ['bash', './src/scripts/setup_iptables_client.sh', self.source, self.destination] )
        else:
            script_exit_code = subprocess.call( ['bash', './src/scripts/setup_iptables_server.sh', self.destination] )

        if script_exit_code != 0:
            print( "Unable to setup iptable rules" )
            self.clear_iptables_rules()
            exit( ExitCodes.IPTABLES_SETUP_ERROR )

    def clear_iptables_rules(self) -> None:
        subprocess.call( ['bash', './src/scripts/clear_iptables.sh'] )

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
            print( f"Next in queue: {packet}    ", end="\r" )
            self.wrap_icmp_and_send( packet )
            return

        if packet.get_mark() == Marks.FROM_CLIENT or packet.get_mark() == Marks.FROM_SERVER:
            self.unwrap_icmp_and_recieve( packet )
            return

        packet.accept()

    def wrap_icmp_and_send(self, packet: Packet) -> None:
        icmp_packet = ICMPPacket( self.destination )
        icmp_packet.payload = packet.get_payload()

        if packet.get_mark() == Marks.TO_CLIENT:
            icmp_packet.payload[16:20] = convert_ip_address_to_bytes( self.destination )

        self.icmp_socket.sendto( icmp_packet.get_raw(), ( self.destination, 1001 ))
        packet.drop()

    def unwrap_icmp_and_recieve(self, packet: Packet) -> None:
        raw_icmp = packet.get_payload()
        secret_payload = bytearray( raw_icmp[8:] )

        if packet.get_mark() == Marks.FROM_CLIENT:
            secret_payload[12:16] = convert_ip_address_to_bytes( self.source )
        
        packet.set_payload( bytes( secret_payload ) )
        packet.repeat()