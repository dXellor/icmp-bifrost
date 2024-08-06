from netfilterqueue import Packet
import socket
import sys

from .icmp_packet import ICMPPacket
from utils.enums import ExitCodes

class ICMPDriver:

    def __init__(self, source: str, destination: str) -> None:
        self.socket = None
        self.source = source
        self.destination = destination
        self.open_icmp_socket()

    def open_icmp_socket(self) -> None:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except socket.error as e:
            print(f"Error while initializing ICMP socket: {e}")
            sys.exit(ExitCodes.CANT_OPEN_SOCKET)

    def wrap_icmp_and_send(self, packet: Packet) -> None:
        icmp_packet = ICMPPacket( self.source, self.destination )
        icmp_packet.payload = packet.get_payload()

        self.socket.sendto( icmp_packet.get_raw(), ( self.destination, 1001 ))

    def unwrap_icmp_and_recieve(self, packet: Packet) -> None:
        pass