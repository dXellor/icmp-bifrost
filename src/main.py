from netfilterqueue import NetfilterQueue, Packet

from core import ICMPDriver
from utils.enums import Marks

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

def main():

    icmp_driver = ICMPDriver( '0.0.0.0', '192.168.0.1' ) 
    handle_queue_with_driver = lambda packet: handle_queue( packet, icmp_driver )

    nfqueue = NetfilterQueue()
    nfqueue.bind(1, handle_queue_with_driver)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')

    nfqueue.unbind()

if __name__ == '__main__':
    main()