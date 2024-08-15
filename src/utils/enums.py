from enum import Enum, IntEnum

class ExitCodes(IntEnum):
    SUCCESS = 0
    INVALID_ARGUMENTS = 1
    SETUP_SCRIPT_ERROR = 2
    CANT_OPEN_SOCKET = 3
    CANT_OPEN_TUN = 4
    NET_INTERFACE_MISSING = 5

class Modes(Enum):
    CLIENT = 1,
    SERVER = 2