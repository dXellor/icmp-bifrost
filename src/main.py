from args import get_args
from core import TunnelDriver
from utils.enums import ExitCodes, Modes
from utils.validators import validate_arguments

def display_title():
    title = r"""
_ ____ _   _ ___     ___  _ ____ ____ ____ ____ ___ 
| |    |\_/| |__] __ |__] | |___ |__/ |  | [__   |  
| |___ |   | |       |__] | |    |  \ |__| ___]  |                          
                                                by dXellor
    """
    print(title)

def main():
    args = get_args()
    if not validate_arguments( args ):
        exit( ExitCodes.INVALID_ARGUMENTS ) 

    tunnel_mode = Modes.CLIENT if args.client else Modes.SERVER
    tunnel = TunnelDriver( args.destination, tunnel_mode, args.interface ) 
    tunnel.run()

if __name__ == '__main__':
    display_title()
    main()