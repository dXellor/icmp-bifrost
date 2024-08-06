from args import get_args
from core import TunnelDriver
from utils.enums import ExitCodes, Modes
from utils.validators import validate_arguments

def main():
    args = get_args()
    if not validate_arguments( args ):
        exit( ExitCodes.INVALID_ARGUMENTS ) 

    tunnel_mode = Modes.CLIENT if args.client else Modes.SERVER
    tunnel = TunnelDriver( args.destination, tunnel_mode ) 
    tunnel.run()

if __name__ == '__main__':
    main()