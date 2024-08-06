from netfilterqueue import NetfilterQueue, Packet
import subprocess

from args import get_args
from core import ICMPDriver
from utils.enums import ExitCodes, Marks
from utils.validators import validate_arguments

def handle_queue(packet: Packet, icmp_driver: ICMPDriver) -> None:

    print( packet )

    if packet.get_mark() == Marks.SENDING:
        print('sending')
        icmp_driver.wrap_icmp_and_send( packet )
        packet.drop()
        return

    if packet.get_mark() == Marks.RECEIVING:
        print('receiving')
        # unwrap_icmp( packet )
        packet.drop()
        return

    packet.accept()

def setup_iptables_rules(destination_ip: str, is_client: bool) -> None:
    setup_script = "./src/scripts/setup_iptables_client.sh" if is_client else "./src/scripts/setup_iptables_server.sh"

    script_exit_code = subprocess.call( ['bash', setup_script, destination_ip] )
    if script_exit_code != 0:
        print( "Unable to setup iptable rules" )
        clear_iptables_rules()
        exit( ExitCodes.IPTABLES_SETUP_ERROR )

def clear_iptables_rules() -> None:
    cleanup_script = "./src/scripts/clear_iptables.sh"
    subprocess.call( ['bash', cleanup_script] )

def main():
    args = get_args()
    if not validate_arguments( args ):
        exit( ExitCodes.INVALID_ARGUMENTS ) 

    setup_iptables_rules( args.destination, args.client )

    icmp_driver = ICMPDriver( '0.0.0.0', args.destination ) 
    handle_queue_with_driver = lambda packet: handle_queue( packet, icmp_driver )

    nfqueue = NetfilterQueue()
    nfqueue.bind(1, handle_queue_with_driver)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')

    nfqueue.unbind()
    clear_iptables_rules()
    
if __name__ == '__main__':
    main()