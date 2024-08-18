from netfilterqueue import NetfilterQueue, Packet
import socket
import subprocess
import sys
from threading import Event, Thread
from time import sleep
from tuntap import TunTap

from .icmp_packet import ICMPPacket
from utils.enums import ExitCodes, Modes
from utils.network import get_script_path

class TunnelDriver:

    def __init__(self, destination: str, mode: Modes) -> None:
        self.mode = mode
        self.destination = destination
        self.tun = None
        self.icmp_socket = None        

        self.run_setup_script()
        self.open_tun_interface()
        self.open_icmp_socket()

    def open_tun_interface(self) -> None:
        try:
            self.tun = TunTap( nic_type='Tun', nic_name='tun0b' )
        except:
            print(f"Error while initializing tun interface")
            sys.exit(ExitCodes.CANT_OPEN_TUN)

    def open_icmp_socket(self) -> None:
        try:
            self.icmp_socket = socket.socket( socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP )
        except socket.error as e:
            print(f"Error while initializing socket: {e}")
            sys.exit(ExitCodes.CANT_OPEN_SOCKET)

    def run_setup_script(self) -> None:
        if self.mode == Modes.CLIENT:
            script_exit_code = subprocess.call( ['bash', get_script_path('setup_client.sh'), self.destination] )
        else:
            script_exit_code = subprocess.call( ['bash', get_script_path('setup_server.sh'), self.destination] )

        if script_exit_code != 0:
            print( "Erorr when running setup script" )
            self.run_cleanup_script()
            exit( ExitCodes.SETUP_SCRIPT_ERROR )

    def run_cleanup_script(self) -> None:
        if self.mode == Modes.CLIENT:
            subprocess.call( ['bash', get_script_path('cleanup.sh'), "0", self.destination] )
        else:
            subprocess.call( ['bash', get_script_path('cleanup.sh'), self.destination, "0"] )

    def wrap_into_icmp(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            buffer = self.tun.read()
            if buffer:
                icmp_packet = ICMPPacket( self.destination, self.mode == Modes.SERVER )
                icmp_packet.payload = buffer
                self.icmp_socket.sendto( icmp_packet.get_raw(), ( self.destination, 1001 ) )

    def unwrap_from_icmp(self, stop_event: Event) -> None:
        nfqueue = NetfilterQueue()
        stoppable_handle = lambda packet: self.handle_queue( packet, stop_event )
        nfqueue.bind(1, stoppable_handle)
        try:
            nfqueue.run()
        except Exception:
            print("")
        nfqueue.unbind()    

    def handle_queue(self, packet: Packet, stop_event: Event) -> None: 
        if stop_event.is_set():
            raise Exception
        
        raw_ip_icmp = packet.get_payload()
        complete_header_len = ( raw_ip_icmp[0] & 0xF ) * 4 + 8
        secret_payload = raw_ip_icmp[complete_header_len:]

        self.tun.write(secret_payload)
        packet.drop()

    def run(self) -> None:
        stop_event = Event()
        wrap_into_icmp_worker = Thread( target=self.wrap_into_icmp, args=[stop_event], daemon=True )
        unwrap_from_icmp_worker = Thread( target=self.unwrap_from_icmp, args=[stop_event], daemon=True )

        wrap_into_icmp_worker.start()
        unwrap_from_icmp_worker.start()

        try:
            print("Tunnel is running")
            print("Input keyboard interupt to close it")
            while True:
                print("", end="\r")
        except KeyboardInterrupt:
            print("Closing the tunnel...")
            print("Wait until the queue is empty")
        
        stop_event.set()
        sleep(10)
        self.tun.close()
        self.run_cleanup_script()