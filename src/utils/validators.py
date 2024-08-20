from argparse import Namespace
import socket

def validate_arguments(args: Namespace) -> bool:

    if args.client and args.server:
        print( "Program can be started only in client or only in server mode" )
        return False
    elif not args.client and not args.server:
        print( "Program mode is required" )
        return False

    if not validate_ip( args.destination ):
        print( "Invalid destination address" )
        return False
    
    if args.time and args.time < 0:
        print( "Invalid time set" )
        return False

    return True

def validate_ip(ip: str) -> bool:
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False