from netfilterqueue import NetfilterQueue, Packet
import socket
import subprocess
import sys

from .icmp_packet import ICMPPacket
from utils.enums import Modes, Marks, ExitCodes

class TunnelDriver:

    def __init__(self, destination: str, mode: Modes) -> None:
        self.mode = mode
        self.socket = None
        self.destination = destination
        self.open_icmp_socket()

    def open_icmp_socket(self) -> None:
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

        if packet.get_mark() == Marks.SENDING:
            print('sending')
            self.wrap_icmp_and_send( packet )
            packet.drop()
            return

        if packet.get_mark() == Marks.RECEIVING:
            print('receiving')
            # unwrap_icmp( packet )
            packet.drop()
            return

        packet.accept()

    def wrap_icmp_and_send(self, packet: Packet) -> None:
        icmp_packet = ICMPPacket( self.destination )
        icmp_packet.payload = packet.get_payload()

        self.socket.sendto( icmp_packet.get_raw(), ( self.destination, 1001 ))

    def unwrap_icmp_and_recieve(self, packet: Packet) -> None:
        pass