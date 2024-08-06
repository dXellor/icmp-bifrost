from netfilterqueue import NetfilterQueue, Packet
import socket
import subprocess
import sys

from .icmp_packet import ICMPPacket
from utils.enums import Modes, Marks, ExitCodes
from utils.networks import get_source_ip_address_in_bytes

class TunnelDriver:

    def __init__(self, destination: str, mode: Modes) -> None:
        self.mode = mode
        self.icmp_socket = None
        self.socket = None
        self.destination = destination
        
        self.open_icmp_socket()
        self.open_socket()

    def open_icmp_socket(self) -> None:
        try:
            self.icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except socket.error as e:
            print(f"Error while initializing ICMP socket: {e}")
            sys.exit(ExitCodes.CANT_OPEN_SOCKET)

    def open_socket(self) -> None:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except socket.error as e:
            print(f"Error while initializing ICMP socket: {e}")
            sys.exit(ExitCodes.CANT_OPEN_SOCKET)

    def setup_iptables_rules(self) -> None:
        setup_script = "./src/scripts/setup_iptables_client.sh" if self.mode == Modes.CLIENT else "./src/scripts/setup_iptables_server.sh"

        script_exit_code = subprocess.call( ['bash', setup_script, self.destination] )
        if script_exit_code != 0:
            print( "Unable to setup iptable rules" )
            self.clear_iptables_rules()
            exit( ExitCodes.IPTABLES_SETUP_ERROR )

    def clear_iptables_rules(self) -> None:
        cleanup_script = "./src/scripts/clear_iptables.sh"
        subprocess.call( ['bash', cleanup_script] )

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

        print( packet )

        if packet.get_mark() == Marks.CLIENT_SENDING:
            print('client: sending')
            self.client_wrap_icmp_and_send( packet )
            return

        if packet.get_mark() == Marks.SERVER_RECEIVING:
            print('server: receiving')
            self.server_unwrap_icmp_and_recieve( packet )
            return

        packet.accept()

    def client_wrap_icmp_and_send(self, packet: Packet) -> None:
        icmp_packet = ICMPPacket( self.destination )
        icmp_packet.payload = packet.get_payload()

        self.icmp_socket.sendto( icmp_packet.get_raw(), ( self.destination, 1001 ))
        packet.drop()

    def server_unwrap_icmp_and_recieve(self, packet: Packet) -> None:
        raw_icmp = packet.get_payload()
        secret_payload = bytearray( raw_icmp[8:] )

        secret_payload[12:16] = get_source_ip_address_in_bytes()
        packet.set_payload( secret_payload )
        packet.repeat()