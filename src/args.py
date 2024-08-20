import argparse

def get_args():

    parser = argparse.ArgumentParser(
        description="ICMP tunneling utility"
    )

    parser.add_argument( "-c", "--client", help="Start utility in client mode", action="store_true" )
    parser.add_argument( "-s", "--server", help="Start utility in server mode", action="store_true" )
    parser.add_argument( "-d", "--destination", help="Destination IP address of the ICMP tunnel in dotted-decimal format", type=str, required=True )
    parser.add_argument( "-t", "--time", help="Set for how many seconds should tunnel be open", type=int )

    return parser.parse_args()